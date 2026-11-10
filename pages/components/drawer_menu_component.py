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

    def is_catalog_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Catalog menu item is displayed."""
        return self.is_displayed(self.MENU_CATALOG_ITEM, timeout=timeout)

    def is_webview_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if WebView menu item is displayed."""
        return self.is_displayed(self.MENU_WEBVIEW_ITEM, timeout=timeout)

    def is_qr_code_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if QR Code Scanner menu item is displayed."""
        return self.is_displayed(self.MENU_QR_CODE_ITEM, timeout=timeout)

    def is_geo_location_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Geo Location menu item is displayed."""
        return self.is_displayed(self.MENU_GEO_LOCATION_ITEM, timeout=timeout)

    def is_drawing_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Drawing menu item is displayed."""
        return self.is_displayed(self.MENU_DRAWING_ITEM, timeout=timeout)

    def is_about_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if About menu item is displayed."""
        return self.is_displayed(self.MENU_ABOUT_ITEM, timeout=timeout)

    def is_reset_app_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Reset App State menu item is displayed."""
        return self.is_displayed(self.MENU_RESET_APP_ITEM, timeout=timeout)

    def is_fingerprint_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if FingerPrint menu item is displayed."""
        return self.is_displayed(self.MENU_FINGERPRINT_ITEM, timeout=timeout)

    def is_virtual_usb_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Virtual USB menu item is displayed."""
        return self.is_displayed(self.MENU_VIRTUAL_USB_ITEM, timeout=timeout)

    def is_crash_app_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Crash app menu item is displayed."""
        return self.is_displayed(self.MENU_CRASH_APP_ITEM, timeout=timeout)

    def is_login_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Login menu item is displayed."""
        return self.is_displayed(self.MENU_LOGIN_ITEM, timeout=timeout)

    def is_logout_item_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Logout menu item is displayed."""
        return self.is_displayed(self.MENU_LOGOUT_ITEM, timeout=timeout)
