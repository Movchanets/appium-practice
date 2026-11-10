"""Top Header / Action Bar Component Object (COM)."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.components.base_component import BaseComponent
from pages.types import Locator


class HeaderComponent(BaseComponent):
    """Component encapsulating the top app bar across screens."""

    HEADER_TITLE: Locator = (AppiumBy.ACCESSIBILITY_ID, "App logo and name")
    MENU_BUTTON: Locator = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    CART_BUTTON: Locator = (AppiumBy.ACCESSIBILITY_ID, "View cart")
    CART_ICON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")
    CART_BADGE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
    SORT_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortIV")

    def is_title_displayed(self, timeout: float = 5.0) -> bool:
        """Check if header title or logo is visible."""
        return self.is_displayed(self.HEADER_TITLE, timeout=timeout)

    def get_title_text(self) -> str:
        """Retrieve header title text or accessibility description."""
        return self.get_text(self.HEADER_TITLE)

    def click_menu(self) -> None:
        """Tap navigation drawer hamburger menu button."""
        self.click(self.MENU_BUTTON)

    def click_cart(self) -> None:
        """Tap shopping cart button."""
        self.click(self.CART_BUTTON)

    def click_sort(self) -> None:
        """Tap catalog sort filter button."""
        self.click(self.SORT_BUTTON)

    def get_cart_item_count(self) -> int:
        """Extract number of items displayed in cart badge; returns 0 if absent."""
        if not self.is_displayed(self.CART_BADGE, timeout=2.0):
            return 0
        raw_text = self.get_text(self.CART_BADGE, timeout=2.0)
        try:
            return int(raw_text.strip())
        except ValueError:
            return 0
