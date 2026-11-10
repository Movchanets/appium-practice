"""Review submission thank-you dialog modal component."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class ReviewModal(BaseModal):
    """Modal dialog displayed after submitting a rating review."""

    MESSAGE_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortTV")
    CLOSE_BUTTON: Locator = (AppiumBy.ACCESSIBILITY_ID, "Closes review dialog")

    def is_displayed(self, locator: Locator | None = None, timeout: float = 3.0) -> bool:
        """Check if review modal message is visible."""
        target_locator = locator or self.MESSAGE_TEXT
        return super().is_displayed(target_locator, timeout=timeout)

    def get_message(self) -> str:
        """Retrieve review confirmation message text."""
        return self.get_text(self.MESSAGE_TEXT).strip()

    def get_message_text(self) -> str:
        """Retrieve review confirmation message text (alias for get_message)."""
        return self.get_message()

    def is_close_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if close button is visible."""
        return self.is_displayed(self.CLOSE_BUTTON, timeout=timeout)

    def close(self) -> None:
        """Tap Close button to dismiss review modal."""
        self.click(self.CLOSE_BUTTON)
