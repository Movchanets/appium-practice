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
        try:
            return self.get_text(self.COPYRIGHT_TEXT, timeout=3.0)
        except Exception:
            if hasattr(self, "root") and self.root:
                return self.root.text or ""
            raise

    def is_displayed(self, locator: Locator | None = None, timeout: float = 3.0) -> bool:
        """Check if copyright text or footer root is displayed."""
        target_locator = locator or self.COPYRIGHT_TEXT
        return super().is_displayed(target_locator, timeout=timeout)
