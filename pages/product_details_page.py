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
        """Check if product details screen is loaded (hero image and title visible)."""
        return self.is_displayed(self.PRODUCT_IMAGE, timeout=10.0) and self.is_displayed(
            self.PRODUCT_TITLE, timeout=5.0
        )

    def get_title(self) -> str:
        """Retrieve the displayed product title."""
        return self.get_text(self.PRODUCT_TITLE)

    def get_price(self) -> str:
        """Retrieve product price string."""
        return self.get_text(self.PRODUCT_PRICE)

    def scroll_to_description(self, max_swipes: int = 3) -> None:
        """Scroll viewport down until product description is visible."""
        for _ in range(max_swipes):
            if self.is_displayed(self.DESCRIPTION_TEXT, timeout=1.0):
                return
            self.swipe_up()

    def get_description(self) -> str:
        """Retrieve product description text, scrolling down if necessary."""
        if not self.is_displayed(self.DESCRIPTION_TEXT, timeout=1.5):
            self.scroll_to_description()
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

    def is_color_selected(self, color: ProductColor) -> bool:
        """Check if specific color variant is currently selected/active.

        The active color circle has an 'aroundIV' indicator inside the same ViewGroup container.
        """
        color_labels: dict[ProductColor, str] = {
            "black": "Black color",
            "blue": "Blue color",
            "gray": "Gray color",
            "green": "Green color",
        }
        label = color_labels.get(color)
        if not label:
            return False
        xpath = (
            f"//android.view.ViewGroup[android.widget.ImageView[@content-desc='{label}'] "
            "and android.widget.ImageView[@resource-id="
            "'com.saucelabs.mydemoapp.android:id/aroundIV']]"
        )
        return self.is_displayed((AppiumBy.XPATH, xpath), timeout=2.0)

    def go_back(self) -> Self:
        """Navigate back to previous screen (Catalog) via system back."""
        self.driver.back()
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

    def is_image_displayed(self, timeout: float = 3.0) -> bool:
        """Check if product hero image is displayed."""
        return self.is_displayed(self.PRODUCT_IMAGE, timeout=timeout)

    def is_price_displayed(self, timeout: float = 3.0) -> bool:
        """Check if product price is displayed."""
        return self.is_displayed(self.PRODUCT_PRICE, timeout=timeout)

    def is_description_displayed(self, timeout: float = 3.0) -> bool:
        """Check if product description text is displayed, scrolling down if needed."""
        if self.is_displayed(self.DESCRIPTION_TEXT, timeout=timeout):
            return True
        self.scroll_to_description()
        return self.is_displayed(self.DESCRIPTION_TEXT, timeout=timeout)

    def is_highlights_displayed(self, timeout: float = 3.0) -> bool:
        """Check if product highlights header is displayed, scrolling down if needed."""
        if self.is_displayed(self.HIGHLIGHTS_TITLE, timeout=timeout):
            return True
        for _ in range(3):
            if self.is_displayed(self.HIGHLIGHTS_TITLE, timeout=1.0):
                return True
            self.swipe_up()
        return self.is_displayed(self.HIGHLIGHTS_TITLE, timeout=timeout)

    def is_rating_displayed(self, timeout: float = 3.0) -> bool:
        """Check if rating star container is displayed."""
        return self.is_displayed(self.RATING_CONTAINER, timeout=timeout)

    def is_add_to_cart_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Add to Cart button is displayed."""
        return self.is_displayed(self.ADD_TO_CART_BUTTON, timeout=timeout)

    def is_color_displayed(self, color: ProductColor, timeout: float = 2.0) -> bool:
        """Check if specific product color variant button is displayed."""
        color_locators: dict[ProductColor, Locator] = {
            "black": self.COLOR_BLACK,
            "blue": self.COLOR_BLUE,
            "gray": self.COLOR_GRAY,
            "green": self.COLOR_GREEN,
        }
        loc = color_locators.get(color)
        return self.is_displayed(loc, timeout=timeout) if loc else False

    def get_rating_stars_count(self) -> int:
        """Count number of rating star elements visible on product details."""
        count = 0
        for star_locator in (self.STAR_1, self.STAR_2, self.STAR_3, self.STAR_4, self.STAR_5):
            if self.is_displayed(star_locator, timeout=1.0):
                count += 1
        return count
