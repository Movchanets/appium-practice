"""Cart Item Component Object for individual items in the Cart list."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CartItemComponent(BaseComponent):
    """Component representing a single product row inside the Cart screen."""

    IMAGE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productIV")
    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
    PRICE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    COLOR_LABEL: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/colorTitleTV")
    COLOR_ICON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/colorIV")
    MINUS_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/minusIV")
    QUANTITY_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")
    PLUS_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/plusIV")
    REMOVE_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/removeBt")

    def get_title(self) -> str:
        """Retrieve the item title."""
        return self.get_text(self.TITLE)

    def get_price(self) -> str:
        """Retrieve the item price string."""
        return self.get_text(self.PRICE)

    def get_quantity(self) -> int:
        """Retrieve the current item quantity as integer."""
        raw_text = self.get_text(self.QUANTITY_TEXT)
        try:
            return int(raw_text.strip())
        except ValueError:
            return 1

    def increase_quantity(self) -> Self:
        """Tap the plus button to increment quantity."""
        self.click(self.PLUS_BUTTON)
        return self

    def decrease_quantity(self) -> Self:
        """Tap the minus button to decrement quantity."""
        self.click(self.MINUS_BUTTON)
        return self

    def remove_item(self) -> None:
        """Tap the Remove Item button."""
        self.click(self.REMOVE_BUTTON)

    def get_color(self) -> str:
        """Retrieve the product variant color label."""
        return self.get_text(self.COLOR_LABEL)

    def is_color_displayed(self, timeout: float = 2.0) -> bool:
        """Check if color icon or label is displayed."""
        return self.is_displayed(self.COLOR_ICON, timeout=timeout) or self.is_displayed(
            self.COLOR_LABEL, timeout=timeout
        )

    def is_image_displayed(self, timeout: float = 2.0) -> bool:
        """Check if cart item product image is displayed."""
        return self.is_displayed(self.IMAGE, timeout=timeout)

    def is_remove_button_displayed(self, timeout: float = 2.0) -> bool:
        """Check if Remove button is displayed."""
        return self.is_displayed(self.REMOVE_BUTTON, timeout=timeout)
