"""Product Details Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.modals.review_modal import ReviewModal
from pages.types import Locator, ProductColor


class ProductDetailsPage(BasePage):
    """Page Object encapsulating product detail inspection, customization, and add to cart."""

    PRODUCT_TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    PRODUCT_IMAGE: Locator = (AppiumBy.ACCESSIBILITY_ID, "Displays selected product")
    PRODUCT_PRICE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    RATING_CONTAINER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/rattingV")
    STAR_1: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start1IV")
    STAR_2: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start2IV")
    STAR_3: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start3IV")
    STAR_4: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start4IV")
    STAR_5: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start5IV")
    COLOR_BLACK: Locator = (AppiumBy.ACCESSIBILITY_ID, "Black color")
    COLOR_BLUE: Locator = (AppiumBy.ACCESSIBILITY_ID, "Blue color")
    COLOR_GRAY: Locator = (AppiumBy.ACCESSIBILITY_ID, "Gray color")
    COLOR_GREEN: Locator = (AppiumBy.ACCESSIBILITY_ID, "Green color")
    MINUS_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/minusIV")
    QUANTITY_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")
    PLUS_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/plusIV")
    ADD_TO_CART_BUTTON: Locator = (AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")
    HIGHLIGHTS_TITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/productHeightLightsTV",
    )
    DESCRIPTION_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/descTV")

    @property
    def review_modal(self) -> ReviewModal:
        """Access the review modal dialog."""
        return ReviewModal(self.driver)

    def is_loaded(self) -> bool:
        """Check if product title is visible."""
        return self.is_displayed(self.PRODUCT_TITLE, timeout=10.0)

    def get_title(self) -> str:
        """Retrieve the displayed product title."""
        return self.get_text(self.PRODUCT_TITLE)

    def get_price(self) -> str:
        """Retrieve product price string."""
        return self.get_text(self.PRODUCT_PRICE)

    def get_description(self) -> str:
        """Retrieve product description text."""
        return self.get_text(self.DESCRIPTION_TEXT)

    def select_color(self, color: ProductColor) -> Self:
        """Select a color variant by name."""
        color_locators: dict[ProductColor, Locator] = {
            "black": self.COLOR_BLACK,
            "blue": self.COLOR_BLUE,
            "gray": self.COLOR_GRAY,
            "green": self.COLOR_GREEN,
        }
        locator = color_locators.get(color)
        if locator is None:
            raise ValueError(f"Unknown color: {color}")
        self.click(locator)
        return self

    def get_quantity(self) -> int:
        """Retrieve current item quantity value."""
        raw_text = self.get_text(self.QUANTITY_TEXT)
        try:
            return int(raw_text.strip())
        except ValueError:
            return 1

    def increase_quantity(self, times: int = 1) -> Self:
        """Tap plus button specified number of times."""
        for _ in range(times):
            self.click(self.PLUS_BUTTON)
        return self

    def decrease_quantity(self, times: int = 1) -> Self:
        """Tap minus button specified number of times."""
        for _ in range(times):
            self.click(self.MINUS_BUTTON)
        return self

    def add_to_cart(self) -> Self:
        """Tap Add to Cart button."""
        self.click(self.ADD_TO_CART_BUTTON)
        return self

    def click_rating_star(self, star: int = 5) -> Self:
        """Tap rating star (1 through 5) opening the review modal."""
        star_map: dict[int, Locator] = {
            1: self.STAR_1,
            2: self.STAR_2,
            3: self.STAR_3,
            4: self.STAR_4,
            5: self.STAR_5,
        }
        locator = star_map.get(star, self.STAR_5)
        self.click(locator)
        return self
