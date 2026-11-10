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
    URL_ERROR: Locator = (
        AppiumBy.XPATH,
        '//*[@resource-id="com.saucelabs.mydemoapp.android:id/urlErrorTV"'
        ' or contains(@text, "URL") or contains(@text, "https")'
        ' or contains(@text, "Please enter")]',
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

    def get_url_error(self) -> str:
        """Retrieve URL format or security error text."""
        return self.get_text(self.URL_ERROR)

    def is_url_error_displayed(self, timeout: float = 3.0) -> bool:
        """Check if URL error warning is displayed."""
        return self.is_displayed(self.URL_ERROR, timeout=timeout)
