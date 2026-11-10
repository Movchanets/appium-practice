"""Checkout Payment Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class CheckoutPaymentPage(BasePage):
    """Page Object encapsulating checkout payment method input and verification."""

    TITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/enterPaymentTitleTV",
    )
    SUBTITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/enterPaymentMethodTV",
    )
    NAME_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
    NAME_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
    CARD_NUMBER_INPUT: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/cardNumberET",
    )
    CARD_NUMBER_ERROR: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/cardNumberErrorTV",
    )
    EXPIRATION_DATE_INPUT: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/expirationDateET",
    )
    EXPIRATION_DATE_ERROR: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/expirationDateErrorTV",
    )
    SECURITY_CODE_INPUT: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/securityCodeET",
    )
    SECURITY_CODE_ERROR: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/securityCodeErrorTV",
    )
    BILLING_SAME_CHECKBOX: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Select if User billing address and shipping address are same",
    )
    REVIEW_ORDER_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Saves payment info and launches screen to review checkout data",
    )

    def is_loaded(self) -> bool:
        """Check if payment entry form is visible."""
        return self.is_displayed(self.NAME_INPUT, timeout=5.0)

    def enter_card_holder_name(self, name: str) -> Self:
        """Fill Card Holder Name field."""
        self.send_keys(self.NAME_INPUT, name)
        return self

    def enter_card_number(self, card_number: str) -> Self:
        """Fill Card Number field."""
        self.send_keys(self.CARD_NUMBER_INPUT, card_number)
        return self

    def enter_expiration_date(self, exp_date: str) -> Self:
        """Fill Expiration Date field (MM/YY)."""
        self.send_keys(self.EXPIRATION_DATE_INPUT, exp_date)
        return self

    def enter_security_code(self, security_code: str) -> Self:
        """Fill Security Code field."""
        self.send_keys(self.SECURITY_CODE_INPUT, security_code)
        return self

    def toggle_billing_same_as_shipping(self, enable: bool = True) -> Self:
        """Set checkbox state for 'My billing address is the same as my shipping address'."""
        element = self.find_element(self.BILLING_SAME_CHECKBOX)
        is_checked = element.get_attribute("checked") == "true"
        if is_checked != enable:
            element.click()
        return self

    def fill_payment_details(
        self,
        name: str,
        card_number: str,
        expiration_date: str,
        security_code: str,
        billing_same: bool = True,
    ) -> Self:
        """Fill complete payment form."""
        self.enter_card_holder_name(name)
        self.enter_card_number(card_number)
        self.enter_expiration_date(expiration_date)
        self.enter_security_code(security_code)
        self.toggle_billing_same_as_shipping(billing_same)
        self.hide_keyboard()
        return self

    def proceed_to_review(self) -> Self:
        """Tap 'Review Order' button."""
        self.click(self.REVIEW_ORDER_BUTTON)
        return self

    def get_name_error(self) -> str:
        """Retrieve full name error text."""
        return self.get_text(self.NAME_ERROR)

    def get_card_number_error(self) -> str:
        """Retrieve card number error text."""
        return self.get_text(self.CARD_NUMBER_ERROR)

    def get_expiration_date_error(self) -> str:
        """Retrieve expiration date error text."""
        return self.get_text(self.EXPIRATION_DATE_ERROR)

    def get_security_code_error(self) -> str:
        """Retrieve security code error text."""
        return self.get_text(self.SECURITY_CODE_ERROR)
