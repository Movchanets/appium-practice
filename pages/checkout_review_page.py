"""Checkout Order Review Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class CheckoutReviewPage(BasePage):
    """Page Object encapsulating checkout order summary review and final submission."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV")
    SUBTITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/enterShippingAddressTV",
    )
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

    def get_card_holder(self) -> str:
        """Retrieve payment cardholder name."""
        return self.get_text(self.CARD_HOLDER)

    def get_card_number(self) -> str:
        """Retrieve masked payment card number."""
        return self.get_text(self.CARD_NUMBER)

    def get_total_items(self) -> str:
        """Retrieve total item count description text."""
        return self.get_text(self.ITEM_NUMBER)

    def get_total_amount(self) -> str:
        """Retrieve order total amount string (e.g. '$ 59.98')."""
        return self.get_text(self.TOTAL_AMOUNT)

    def place_order(self) -> Self:
        """Tap 'Place Order' button to submit order."""
        self.click(self.PLACE_ORDER_BUTTON)
        return self
