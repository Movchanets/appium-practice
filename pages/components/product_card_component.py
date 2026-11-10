"""Product Card Component Object for individual catalog items."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ProductCardComponent(BaseComponent):
    """Component representing a single product card in the catalog grid."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
    PRICE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    IMAGE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productIV")
    RATING_CONTAINER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/rattingV")
    STAR_1: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start1IV")
    STAR_2: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start2IV")
    STAR_3: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start3IV")
    STAR_4: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start4IV")
    STAR_5: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/start5IV")

    def get_title(self) -> str:
        """Retrieve the product item title."""
        try:
            return self.get_text(self.TITLE, timeout=2.0)
        except Exception:
            return self.root.text or ""

    def get_price(self) -> str:
        """Retrieve the product price text (e.g. '$ 29.99')."""
        try:
            return self.get_text(self.PRICE, timeout=2.0)
        except Exception:
            return ""

    def click_item(self) -> None:
        """Tap this product item to navigate to its details screen."""
        self.root.click()

    def click_image(self) -> None:
        """Tap product image thumbnail."""
        self.click(self.IMAGE)

    def click_rating_star(self, star: int = 5) -> None:
        """Tap a specific rating star (1 through 5)."""
        star_locators: dict[int, Locator] = {
            1: self.STAR_1,
            2: self.STAR_2,
            3: self.STAR_3,
            4: self.STAR_4,
            5: self.STAR_5,
        }
        locator = star_locators.get(star, self.STAR_5)
        self.click(locator)
