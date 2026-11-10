"""WebView Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class WebViewPage(BasePage):
    """Page Object encapsulating WebView URL browser demo screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/webViewTV")
    URL_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/urlET")
    GO_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Tap to view content of given url",
    )

    def is_loaded(self) -> bool:
        """Check if WebView page title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def enter_url(self, url: str) -> Self:
        """Fill URL address input field."""
        self.send_keys(self.URL_INPUT, url)
        return self

    def click_go(self) -> Self:
        """Tap Go button to load the entered URL."""
        self.click(self.GO_BUTTON)
        return self

    def load_url(self, url: str) -> Self:
        """Enter URL and submit to load in webview."""
        self.enter_url(url)
        self.hide_keyboard()
        self.click_go()
        return self
