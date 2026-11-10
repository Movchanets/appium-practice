"""Checkout Complete Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class CheckoutCompletePage(BasePage):
    """Page Object encapsulating order confirmation success screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/completeTV")
    THANK_YOU_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/thankYouTV")
    DISPATCH_INFO: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/swagTV")
    CONTINUE_SHOPPING_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Tap to open catalog",
    )

    def is_loaded(self) -> bool:
        """Check if checkout complete screen is displayed."""
        return self.is_displayed(self.CONTINUE_SHOPPING_BUTTON, timeout=5.0)

    def get_thank_you_message(self) -> str:
        """Retrieve thank you heading message text."""
        return self.get_text(self.THANK_YOU_TEXT)

    def get_dispatch_message(self) -> str:
        """Retrieve order dispatch info description."""
        return self.get_text(self.DISPATCH_INFO)

    def click_continue_shopping(self) -> Self:
        """Tap 'Continue Shopping' button to return to catalog."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self
