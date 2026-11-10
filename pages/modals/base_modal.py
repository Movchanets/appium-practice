"""Base Component Object Model (COM) class for modal dialogs and alert popups."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base
from pages.types import Locator


class BaseModal(Base):
    """Base Component Object Model representing dialogs and alert popups."""

    MODAL_CONTAINER: Locator = (AppiumBy.ID, "android:id/parentPanel")
    MODAL_TITLE: Locator = (AppiumBy.ID, "android:id/alertTitle")
    MODAL_MESSAGE: Locator = (AppiumBy.ID, "android:id/message")
    CONFIRM_BUTTON: Locator = (AppiumBy.ID, "android:id/button1")
    CANCEL_BUTTON: Locator = (AppiumBy.ID, "android:id/button2")

    def __init__(self, context: WebDriver | WebElement) -> None:
        """Initialize modal with WebDriver or WebElement context."""
        super().__init__(context)

    def is_displayed(self, locator: Locator | None = None, timeout: float = 3.0) -> bool:
        """Check if dialog container or specific locator is currently visible."""
        target_locator = locator or self.MODAL_CONTAINER
        return super().is_displayed(target_locator, timeout=timeout)

    def get_title_text(self) -> str:
        """Retrieve the trimmed text of the dialog title."""
        return self.get_text(self.MODAL_TITLE).strip()

    def get_message_text(self) -> str:
        """Retrieve the trimmed text of the dialog body message."""
        return self.get_text(self.MODAL_MESSAGE).strip()

    def confirm(self) -> None:
        """Click the primary affirmative action button (e.g. OK / Log Out)."""
        self.click(self.CONFIRM_BUTTON)

    def dismiss(self) -> None:
        """Click the cancel/negative action button."""
        self.click(self.CANCEL_BUTTON)
