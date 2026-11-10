"""Slide Navigation Drawer Menu Component Object (COM)."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.components.base_component import BaseComponent
from pages.types import Locator


class DrawerMenuComponent(BaseComponent):
    """Component encapsulating the slide navigation drawer menu and its actions."""

    MENU_CATALOG_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Catalog"]',
    )
    MENU_WEBVIEW_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="WebView"]',
    )
    MENU_QR_CODE_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="QR Code Scanner"]',
    )
    MENU_GEO_LOCATION_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Geo Location"]',
    )
    MENU_DRAWING_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Drawing"]',
    )
    MENU_ABOUT_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="About"]',
    )
    MENU_RESET_APP_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Reset App State"]',
    )
    MENU_FINGERPRINT_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="FingerPrint"]',
    )
    MENU_VIRTUAL_USB_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Virtual USB"]',
    )
    MENU_CRASH_APP_ITEM: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/itemTV"'
        ' and @text="Crash app (debug)"]',
    )
    MENU_LOGIN_ITEM: Locator = (AppiumBy.ACCESSIBILITY_ID, "Login Menu Item")
    MENU_LOGOUT_ITEM: Locator = (AppiumBy.ACCESSIBILITY_ID, "Logout Menu Item")
    LOGOUT_CONFIRM_BUTTON: Locator = (AppiumBy.ID, "android:id/button1")

    def is_open(self, timeout: float = 1.5) -> bool:
        """Check if drawer menu root element is currently displayed."""
        return self.is_visible()

    def is_logged_in(self, timeout: float = 2.0) -> bool:
        """Check if logout item is displayed indicating an active user session."""
        return self.is_displayed(self.MENU_LOGOUT_ITEM, timeout=timeout)

    def click_catalog(self) -> None:
        """Tap Catalog drawer menu item."""
        self.click(self.MENU_CATALOG_ITEM)

    def click_webview(self) -> None:
        """Tap WebView drawer menu item."""
        self.click(self.MENU_WEBVIEW_ITEM)

    def click_qr_code_scanner(self) -> None:
        """Tap QR Code Scanner drawer menu item."""
        self.click(self.MENU_QR_CODE_ITEM)

    def click_geo_location(self) -> None:
        """Tap Geo Location drawer menu item."""
        self.click(self.MENU_GEO_LOCATION_ITEM)

    def click_drawing(self) -> None:
        """Tap Drawing drawer menu item."""
        self.click(self.MENU_DRAWING_ITEM)

    def click_about(self) -> None:
        """Tap About drawer menu item."""
        self.click(self.MENU_ABOUT_ITEM)

    def click_reset_app_state(self) -> None:
        """Tap Reset App State drawer menu item."""
        self.click(self.MENU_RESET_APP_ITEM)

    def click_fingerprint(self) -> None:
        """Tap FingerPrint drawer menu item."""
        self.click(self.MENU_FINGERPRINT_ITEM)

    def click_virtual_usb(self) -> None:
        """Tap Virtual USB drawer menu item."""
        self.click(self.MENU_VIRTUAL_USB_ITEM)

    def click_crash_app(self) -> None:
        """Tap Crash app drawer menu item."""
        self.click(self.MENU_CRASH_APP_ITEM)

    def click_login(self) -> None:
        """Tap Login drawer menu item."""
        self.click(self.MENU_LOGIN_ITEM)

    def click_logout(self) -> None:
        """Tap Logout drawer menu item."""
        self.click(self.MENU_LOGOUT_ITEM)

    def logout_if_logged_in(self) -> None:
        """Perform graceful logout and confirm dialog if session is active."""
        if self.is_logged_in(timeout=2.0):
            self.click_logout()
            try:
                confirm_btn = self._wait_clickable(
                    self.LOGOUT_CONFIRM_BUTTON, timeout=3.0, from_driver=True
                )
                confirm_btn.click()
            except (TimeoutException, NoSuchElementException):
                pass
