"""About Screen Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class AboutPage(BasePage):
    """Page Object encapsulating About screen with app version and external website link."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/aboutTV")
    VERSION_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/versionTV")
    WEB_LINK: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/webTV")

    def is_loaded(self) -> bool:
        """Check if About screen title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def get_version(self) -> str:
        """Retrieve displayed application version string."""
        return self.get_text(self.VERSION_TEXT)

    def click_web_link(self) -> Self:
        """Tap website URL link."""
        self.click(self.WEB_LINK)
        return self
