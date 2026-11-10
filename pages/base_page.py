"""Base Page Object implementation providing core actions, waits, and W3C gestures."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base
from pages.components.drawer_menu_component import DrawerMenuComponent
from pages.components.header_component import HeaderComponent
from pages.types import Locator


class BasePage(Base):
    """Foundational Page Object with robust explicit waits and dynamic W3C touch gestures."""

    HEADER_ROOT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/header")
    DRAWER_MENU: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/menuRV")
    PERMISSION_ALLOW_BUTTON: Locator = (
        AppiumBy.XPATH,
        "//*[@resource-id='com.android.permissioncontroller:id/permission_allow_button' "
        "or @resource-id='com.android.packageinstaller:id/permission_allow_button']",
    )
    PERMISSION_DENY_BUTTON: Locator = (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_deny_button",
    )
    SCROLLABLE_TEXT_LOCATOR: Locator = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        "new UiScrollable(new UiSelector().scrollable(true))"
        '.scrollIntoView(new UiSelector().textContains("{text}"))',
    )
    TEXT_CONTAINS_LOCATOR: Locator = (
        AppiumBy.XPATH,
        "//*[contains(@text, '{text}')]",
    )

    def __init__(self, driver: WebDriver) -> None:
        """Initialize the page object with a mobile WebDriver instance."""
        super().__init__(driver)

    @property
    def header(self) -> HeaderComponent:
        """Access the top HeaderComponent."""
        header_el = self.find_element(self.HEADER_ROOT)
        return HeaderComponent(header_el)

    @property
    def drawer_menu(self) -> DrawerMenuComponent:
        """Access the slide DrawerMenuComponent."""
        drawer_el = self.find_element(self.DRAWER_MENU)
        return DrawerMenuComponent(drawer_el)

    def open_menu(self) -> Self:
        """Tap navigation drawer trigger button if drawer is not already opened."""
        if not self.is_displayed(self.DRAWER_MENU, timeout=1.5):
            self.header.click_menu()
        return self

    # ---------------------------------------------------------
    # Dynamic W3C Gestures (Screen Percentage Calculations)
    # ---------------------------------------------------------

    def swipe(
        self,
        start_x_pct: float,
        start_y_pct: float,
        end_x_pct: float,
        end_y_pct: float,
        duration_ms: int = 800,
    ) -> None:
        """Execute a swipe gesture between dynamic screen percentages via W3C ActionChains."""
        window_size = self.driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        start_x = int(width * start_x_pct)
        start_y = int(height * start_y_pct)
        end_x = int(width * end_x_pct)
        end_y = int(height * end_y_pct)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000.0)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_up(self, duration_ms: int = 800) -> None:
        """Scroll down viewport content by swiping from 80% to 20% vertical height."""
        self.swipe(
            start_x_pct=0.5,
            start_y_pct=0.8,
            end_x_pct=0.5,
            end_y_pct=0.2,
            duration_ms=duration_ms,
        )

    def swipe_down(self, duration_ms: int = 800) -> None:
        """Scroll up viewport content by swiping from 20% to 80% vertical height."""
        self.swipe(
            start_x_pct=0.5,
            start_y_pct=0.2,
            end_x_pct=0.5,
            end_y_pct=0.8,
            duration_ms=duration_ms,
        )

    def swipe_left(self, duration_ms: int = 800) -> None:
        """Swipe viewport leftwards from 80% to 20% horizontal width."""
        self.swipe(
            start_x_pct=0.8,
            start_y_pct=0.5,
            end_x_pct=0.2,
            end_y_pct=0.5,
            duration_ms=duration_ms,
        )

    def swipe_right(self, duration_ms: int = 800) -> None:
        """Swipe viewport rightwards from 20% to 80% horizontal width."""
        self.swipe(
            start_x_pct=0.2,
            start_y_pct=0.5,
            end_x_pct=0.8,
            end_y_pct=0.5,
            duration_ms=duration_ms,
        )

    def scroll_to_text(self, text: str, max_swipes: int = 5) -> WebElement:
        """Scroll dynamically to locate an element containing text.

        First attempts native Android UiScrollable if applicable, then falls back to swipe loop.
        """
        # Attempt Android native UiScrollable
        try:
            scrollable_locator = self.resolve_locator(self.SCROLLABLE_TEXT_LOCATOR, text=text)
            return self.find_element(scrollable_locator, timeout=3.0)
        except Exception:
            pass

        # Cross-platform fallback loop with dynamic swipes
        text_locator = self.resolve_locator(self.TEXT_CONTAINS_LOCATOR, text=text)
        for _ in range(max_swipes):
            try:
                element = self.find_element(text_locator, timeout=1.5)
                if element.is_displayed():
                    return element
            except (TimeoutException, NoSuchElementException):
                self.swipe_up()

        raise NoSuchElementException(
            f"Failed to find element with text '{text}' after {max_swipes} dynamic swipes."
        )

    def tap_by_coordinates(self, x_pct: float, y_pct: float) -> None:
        """Tap a screen position calculated from relative screen percentages."""
        window_size = self.driver.get_window_size()
        x = int(window_size["width"] * x_pct)
        y = int(window_size["height"] * y_pct)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def long_press(self, locator: Locator, duration_s: float = 2.0) -> None:
        """Perform a touch-and-hold (long press) gesture on a targeted element."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to(element)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_s)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    # ---------------------------------------------------------
    # Device State & Lifecycle Helpers
    # ---------------------------------------------------------

    def background_app(self, seconds: int = 5) -> None:
        """Send the mobile application to background for specified seconds, then resume."""
        try:
            self.driver.execute_script("mobile: backgroundApp", {"seconds": seconds})
        except Exception:
            self.driver.background_app(seconds)

    def set_orientation(self, orientation: str) -> None:
        """Set screen orientation (PORTRAIT or LANDSCAPE)."""
        self.driver.orientation = orientation.upper()

    def get_orientation(self) -> str:
        """Get the current screen orientation in upper case."""
        return str(self.driver.orientation).upper()

    def rotate_to_landscape(self) -> Self:
        """Rotate device orientation to LANDSCAPE."""
        self.set_orientation("LANDSCAPE")
        return self

    def rotate_to_portrait(self) -> Self:
        """Rotate device orientation to PORTRAIT."""
        self.set_orientation("PORTRAIT")
        return self

    def hide_keyboard(self) -> None:
        """Safely hide on-screen soft keyboard if currently open."""
        try:
            self.driver.execute_script("mobile: hideKeyboard")
        except Exception:
            try:
                self.driver.hide_keyboard()
            except Exception:
                pass

    def handle_permission_alert(self, allow: bool = True) -> None:
        """Handle OS runtime system permission prompts."""
        try:
            alert = self.driver.switch_to.alert
            if allow:
                alert.accept()
            else:
                alert.dismiss()
        except Exception:
            target_locator = self.PERMISSION_ALLOW_BUTTON if allow else self.PERMISSION_DENY_BUTTON
            try:
                btn = self.find_element(target_locator, timeout=2.0)
                btn.click()
            except (TimeoutException, NoSuchElementException):
                pass
