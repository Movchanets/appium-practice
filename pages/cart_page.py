"""Shopping Cart Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import BasePage
from pages.components.cart_item_component import CartItemComponent
from pages.types import Locator


class CartPage(BasePage):
    """Page Object encapsulating shopping cart item review and checkout navigation."""

    # Empty cart elements
    EMPTY_CONTAINER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noItemCL")
    NO_ITEMS_TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noItemTitleTV")
    GO_SHOPPING_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/shoppingBt")

    # Populated cart elements
    CART_ITEMS: Locator = (
        AppiumBy.XPATH,
        '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.saucelabs.mydemoapp.android:id/productRV"]/android.view.ViewGroup',
    )
    TOTAL_ITEMS_LABEL: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/itemsTV")
    TOTAL_PRICE_LABEL: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalPriceTV")
    CHECKOUT_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Confirms products for checkout",
    )

    def is_loaded(self) -> bool:
        """Check if cart screen is loaded (either empty state or items displayed)."""
        return self.is_empty(timeout=3.0) or self.is_displayed(self.CHECKOUT_BUTTON, timeout=3.0)

    def is_empty(self, timeout: float = 3.0) -> bool:
        """Check if cart is currently in empty state."""
        return self.is_displayed(self.EMPTY_CONTAINER, timeout=timeout)

    def click_go_shopping(self) -> Self:
        """Tap 'Go Shopping' button in empty cart."""
        self.click(self.GO_SHOPPING_BUTTON)
        return self

    def get_cart_items(self) -> list[CartItemComponent]:
        """Return list of CartItemComponent instances for all rows."""
        elements = self.find_elements(self.CART_ITEMS)
        return [CartItemComponent(el) for el in elements]

    def get_cart_item_by_title(self, title: str) -> CartItemComponent:
        """Find a single cart item component matching product title."""
        for item in self.get_cart_items():
            if title in item.get_title():
                return item
        raise NoSuchElementException(f"Cart item with title '{title}' not found")

    def get_total_items_count(self) -> int:
        """Retrieve total item count integer from items label."""
        raw_text = self.get_text(self.TOTAL_ITEMS_LABEL)
        try:
            return int(raw_text.split()[0])
        except (ValueError, IndexError):
            return 0

    def get_total_price(self) -> str:
        """Retrieve total price string."""
        return self.get_text(self.TOTAL_PRICE_LABEL)

    def proceed_to_checkout(self) -> Self:
        """Tap Proceed To Checkout button."""
        self.click(self.CHECKOUT_BUTTON)
        return self

    def is_go_shopping_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Go Shopping button is displayed."""
        return self.is_displayed(self.GO_SHOPPING_BUTTON, timeout=timeout)

    def is_checkout_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Proceed to Checkout button is displayed."""
        return self.is_displayed(self.CHECKOUT_BUTTON, timeout=timeout)

    def is_total_price_displayed(self, timeout: float = 3.0) -> bool:
        """Check if total price label is displayed."""
        return self.is_displayed(self.TOTAL_PRICE_LABEL, timeout=timeout)

    def is_total_items_displayed(self, timeout: float = 3.0) -> bool:
        """Check if total items count label is displayed."""
        return self.is_displayed(self.TOTAL_ITEMS_LABEL, timeout=timeout)
