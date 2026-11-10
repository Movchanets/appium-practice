"""Footer Component Object for copyright banner."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.components.base_component import BaseComponent
from pages.types import Locator


class FooterComponent(BaseComponent):
    """Component representing footer info and copyright text."""

    COPYRIGHT_TEXT: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[contains(@text, "Sauce Labs All Rights Reserved")]',
    )

    def get_copyright_text(self) -> str:
        """Retrieve the copyright text string."""
        return self.get_text(self.COPYRIGHT_TEXT)
