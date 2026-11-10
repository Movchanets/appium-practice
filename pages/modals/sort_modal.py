"""Sort selection dialog modal component."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.modals.base_modal import BaseModal
from pages.types import Locator, SortOption


class SortModal(BaseModal):
    """Modal dialog for sorting catalog products."""

    MODAL_CONTAINER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortTV")
    NAME_ASC: Locator = (AppiumBy.ACCESSIBILITY_ID, "Ascending order by name")
    NAME_DESC: Locator = (AppiumBy.ACCESSIBILITY_ID, "Descending order by name")
    PRICE_ASC: Locator = (AppiumBy.ACCESSIBILITY_ID, "Ascending order by price")
    PRICE_DESC: Locator = (AppiumBy.ACCESSIBILITY_ID, "Descending order by price")

    def is_displayed(self, locator: Locator | None = None, timeout: float = 3.0) -> bool:
        """Check if sort dialog options are visible."""
        target_locator = locator or self.NAME_ASC
        return super().is_displayed(target_locator, timeout=timeout)

    def select_option(self, option: SortOption) -> None:
        """Select a sorting option by key."""
        options_map: dict[SortOption, Locator] = {
            "name_asc": self.NAME_ASC,
            "name_desc": self.NAME_DESC,
            "price_asc": self.PRICE_ASC,
            "price_desc": self.PRICE_DESC,
        }
        target = options_map.get(option)
        if target is None:
            raise ValueError(f"Unknown sort option: {option}")
        self.click(target)

    def sort_by_name_ascending(self) -> None:
        """Sort by name ascending."""
        self.select_option("name_asc")

    def sort_by_name_descending(self) -> None:
        """Sort by name descending."""
        self.select_option("name_desc")

    def sort_by_price_ascending(self) -> None:
        """Sort by price ascending."""
        self.select_option("price_asc")

    def sort_by_price_descending(self) -> None:
        """Sort by price descending."""
        self.select_option("price_desc")
