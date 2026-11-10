"""QR Code Scanner Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class QrCodeScannerPage(BasePage):
    """Page Object encapsulating QR Code Scanner screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/qrCodeTV")
    VIEWFINDER: Locator = (
        AppiumBy.XPATH,
        '//*[@resource-id="com.saucelabs.mydemoapp.android:id/barcodeScannerView"'
        ' or @resource-id="com.saucelabs.mydemoapp.android:id/scannerV"'
        ' or @resource-id="com.saucelabs.mydemoapp.android:id/qrCodeTV"]',
    )

    def is_loaded(self) -> bool:
        """Check if QR Code Scanner title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def get_title_text(self) -> str:
        """Retrieve screen title text."""
        return self.get_text(self.TITLE)

    def grant_camera_permission(self, allow: bool = True) -> Self:
        """Handle system camera permission alert."""
        self.handle_permission_alert(allow=allow)
        return self

    def is_viewfinder_displayed(self, timeout: float = 3.0) -> bool:
        """Check if scanner viewfinder or camera frame is displayed."""
        return self.is_displayed(self.VIEWFINDER, timeout=timeout)
