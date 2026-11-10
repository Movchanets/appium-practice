"""QR Code Scanner Page Object."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class QrCodeScannerPage(BasePage):
    """Page Object encapsulating QR Code Scanner screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/qrCodeTV")

    def is_loaded(self) -> bool:
        """Check if QR Code Scanner title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def get_title_text(self) -> str:
        """Retrieve screen title text."""
        return self.get_text(self.TITLE)
