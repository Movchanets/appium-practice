"""Unified Base class for Page Object Model (POM) and Component Object Model (COM).

Inspired by production architectural patterns:
- Supports both WebDriver (Page Objects) and WebElement (Component Objects) contexts.
- Automatically restricts XPath selectors to component scope via relative prefixing ('.//').
- Encapsulates explicit synchronization, robust error tolerance, and element interactions.
"""

from __future__ import annotations

from typing import Literal, cast

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pages.types import Locator


class Base:
    """Foundational class for both Page Objects and Component Objects."""

    driver: WebDriver
    root: WebElement | None

    def __init__(self, context: WebDriver | WebElement) -> None:
        """Initialize the base object with a WebDriver or WebElement context."""
        if isinstance(context, WebDriver):
            self.driver = context
            self.root = None
        elif isinstance(context, WebElement):
            self.root = context
            self.driver = cast(WebDriver, context.parent)
        else:
            raise TypeError(f"Invalid context type: {type(context)}")

    @property
    def _target(self) -> WebDriver | WebElement:
        """Return active searching context (root WebElement if inside component, else driver)."""
        return self.root if self.root is not None else self.driver

    def get_wait(self, timeout: float = 10.0) -> WebDriverWait[WebDriver]:
        """Return a WebDriverWait instance bound to the driver with standard ignored exceptions."""
        return WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
                ElementNotInteractableException,
            ),
        )

    @property
    def wait(self) -> WebDriverWait[WebDriver]:
        """Default explicit wait instance (10.0s)."""
        return self.get_wait(10.0)

    def _format_locator(self, locator: Locator) -> Locator:
        """Ensure XPath selectors search within root element context by prepending dot if needed."""
        by, value = locator
        if self.root is not None and (by in (By.XPATH, AppiumBy.XPATH)) and value.startswith("//"):
            return (by, "." + value)
        return locator

    def _find_element(self, locator: Locator, from_driver: bool = False) -> WebElement:
        """Find a single element within the active context or optionally root driver."""
        target = self._target if not from_driver else self.driver
        return target.find_element(*self._format_locator(locator))

    def _find_elements(self, locator: Locator, from_driver: bool = False) -> list[WebElement]:
        """Find all matching elements within active context or optionally root driver."""
        target = self._target if not from_driver else self.driver
        return cast(list[WebElement], target.find_elements(*self._format_locator(locator)))

    def _wait_present(self, locator: Locator, timeout: float = 10.0) -> WebElement:
        """Wait until an element exists in the DOM/view hierarchy."""
        return self.get_wait(timeout).until(
            lambda _: self._find_element(locator),
            message=f"Element with locator {locator} was not present within {timeout}s",
        )

    def _wait_visible(self, locator: Locator, timeout: float = 10.0) -> WebElement:
        """Wait until an element is visible within the active context."""

        def _predicate(_: object) -> WebElement | Literal[False]:
            try:
                element = self._find_element(locator)
                return element if element.is_displayed() else False
            except Exception:
                return False

        return self.get_wait(timeout).until(
            _predicate,
            message=f"Element with locator {locator} was not visible within {timeout}s",
        )

    def _wait_clickable(
        self, locator: Locator, timeout: float = 10.0, from_driver: bool = False
    ) -> WebElement:
        """Wait until an element is clickable (visible and enabled) within active context."""

        def _predicate(_: object) -> WebElement | Literal[False]:
            try:
                element = self._find_element(locator, from_driver=from_driver)
                return element if (element.is_displayed() and element.is_enabled()) else False
            except Exception:
                return False

        return self.get_wait(timeout).until(
            _predicate,
            message=f"Element with locator {locator} was not clickable within {timeout}s",
        )

    # ---------------------------------------------------------
    # Core Public Interaction Primitives
    # ---------------------------------------------------------

    def find_element(self, locator: Locator, timeout: float = 10.0) -> WebElement:
        """Find an element on the screen waiting until it is present."""
        return self._wait_present(locator, timeout=timeout)

    def find_elements(self, locator: Locator, timeout: float = 10.0) -> list[WebElement]:
        """Find all elements matching locator, returning empty list if none found within timeout."""
        try:
            self._wait_present(locator, timeout=timeout)
            return self._find_elements(locator)
        except TimeoutException:
            return []

    def click(self, locator: Locator, timeout: float = 10.0) -> None:
        """Wait until element is clickable and perform click."""
        element = self._wait_clickable(locator, timeout=timeout)
        element.click()

    def send_keys(
        self,
        locator: Locator,
        text: str,
        clear: bool = True,
        timeout: float = 10.0,
    ) -> None:
        """Wait for element visibility, optionally clear existing content, and type text."""
        element = self._wait_visible(locator, timeout=timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator, timeout: float = 10.0) -> str:
        """Retrieve visible text or content-desc/accessibility label from an element."""
        element = self.find_element(locator, timeout=timeout)
        text = element.text
        if not text:
            text = element.get_attribute("content-desc") or element.get_attribute("text") or ""
        return text

    def is_displayed(self, locator: Locator | None = None, timeout: float = 5.0) -> bool:
        """Check if element or root component is visible without raising uncaught exceptions."""
        try:
            if locator is not None:
                element = self._wait_visible(locator, timeout=timeout)
                return bool(element.is_displayed())
            if self.root is not None:
                return bool(self.root.is_displayed())
            return False
        except (TimeoutException, NoSuchElementException):
            return False
