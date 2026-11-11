"""Checkout Order Review Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.types import Locator


class CheckoutReviewPage(BasePage):
    """Page Object encapsulating checkout order summary review and final submission."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV")
    SUBTITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/enterShippingAddressTV",
    )
    PRODUCT_PRICE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    FULL_NAME: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameTV")
    ADDRESS: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/addressTV")
    CITY: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityTV")
    COUNTRY: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryTV")
    CARD_HOLDER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardHolderTV")
    CARD_NUMBER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberTV")
    ITEM_NUMBER: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/itemNumberTV")
    TOTAL_AMOUNT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV")
    PLACE_ORDER_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Completes the process of checkout",
    )

    def is_loaded(self) -> bool:
        """Check if review order screen is loaded."""
        return self.is_displayed(self.PLACE_ORDER_BUTTON, timeout=5.0)

    def scroll_to_element(self, locator: Locator, max_swipes: int = 3) -> WebElement:
        """Scroll down viewport until element is displayed."""
        for _ in range(max_swipes):
            if self.is_displayed(locator, timeout=1.0):
                return self.find_element(locator)
            self.swipe_up()
        return self.find_element(locator)

    def get_shipping_name(self) -> str:
        """Retrieve shipping full name."""
        return self.get_text(self.FULL_NAME)

    def get_shipping_address(self) -> str:
        """Retrieve shipping street address."""
        return self.get_text(self.ADDRESS)

    def get_shipping_city(self) -> str:
        """Retrieve shipping city / state / zip info."""
        return self.get_text(self.CITY)

    def get_shipping_country(self) -> str:
        """Retrieve shipping country."""
        return self.get_text(self.COUNTRY)

    def get_product_price(self) -> str:
        """Retrieve product price string on review screen."""
        return self.get_text(self.PRODUCT_PRICE)

    def get_card_holder(self) -> str:
        """Retrieve payment cardholder name, scrolling if needed."""
        if not self.is_displayed(self.CARD_HOLDER, timeout=1.5):
            self.scroll_to_element(self.CARD_HOLDER)
        return self.get_text(self.CARD_HOLDER)

    def get_card_number(self) -> str:
        """Retrieve masked payment card number, scrolling if needed."""
        if not self.is_displayed(self.CARD_NUMBER, timeout=1.5):
            self.scroll_to_element(self.CARD_NUMBER)
        return self.get_text(self.CARD_NUMBER)

    def get_total_items(self) -> str:
        """Retrieve total item count description text."""
        return self.get_text(self.ITEM_NUMBER)

    def get_total_amount(self) -> str:
        """Retrieve order total amount string (e.g. '$ 59.98'), scrolling if needed."""
        if not self.is_displayed(self.TOTAL_AMOUNT, timeout=1.5):
            self.scroll_to_element(self.TOTAL_AMOUNT)
        return self.get_text(self.TOTAL_AMOUNT)

    def place_order(self) -> Self:
        """Tap 'Place Order' button to submit order."""
        self.click(self.PLACE_ORDER_BUTTON)
        return self
