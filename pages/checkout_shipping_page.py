"""Checkout Shipping Address Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class CheckoutShippingPage(BasePage):
    """Page Object encapsulating checkout shipping address input and validation."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV")
    SUBTITLE: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/enterShippingAddressTV",
    )
    FULL_NAME_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET")
    FULL_NAME_ERROR: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/fullNameErrorTV",
    )
    ADDRESS_1_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET")
    ADDRESS_1_ERROR: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/address1ErrorTV",
    )
    ADDRESS_2_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET")
    CITY_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET")
    CITY_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityErrorTV")
    STATE_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/stateET")
    ZIP_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET")
    ZIP_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipErrorTV")
    COUNTRY_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET")
    COUNTRY_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryErrorTV")
    TO_PAYMENT_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Saves user info for checkout",
    )

    def is_loaded(self) -> bool:
        """Check if shipping address form is visible."""
        return self.is_displayed(self.FULL_NAME_INPUT, timeout=5.0)

    def enter_full_name(self, name: str) -> Self:
        """Fill Full Name input field."""
        self.send_keys(self.FULL_NAME_INPUT, name)
        return self

    def enter_address_line_1(self, address: str) -> Self:
        """Fill Address Line 1 input field."""
        self.send_keys(self.ADDRESS_1_INPUT, address)
        return self

    def enter_address_line_2(self, address: str) -> Self:
        """Fill optional Address Line 2 input field."""
        self.send_keys(self.ADDRESS_2_INPUT, address)
        return self

    def enter_city(self, city: str) -> Self:
        """Fill City input field."""
        self.send_keys(self.CITY_INPUT, city)
        return self

    def enter_state(self, state: str) -> Self:
        """Fill State/Region input field."""
        self.send_keys(self.STATE_INPUT, state)
        return self

    def enter_zip(self, zip_code: str) -> Self:
        """Fill Zip/Postal Code input field."""
        self.send_keys(self.ZIP_INPUT, zip_code)
        return self

    def enter_country(self, country: str) -> Self:
        """Fill Country input field."""
        self.send_keys(self.COUNTRY_INPUT, country)
        return self

    def fill_shipping_details(
        self,
        full_name: str,
        address_1: str,
        city: str,
        zip_code: str,
        country: str,
        state: str = "",
        address_2: str = "",
    ) -> Self:
        """Fill entire shipping address form."""
        self.enter_full_name(full_name)
        self.enter_address_line_1(address_1)
        if address_2:
            self.enter_address_line_2(address_2)
        self.enter_city(city)
        if state:
            self.enter_state(state)
        self.enter_zip(zip_code)
        self.enter_country(country)
        self.hide_keyboard()
        return self

    def proceed_to_payment(self) -> Self:
        """Tap 'To Payment' button."""
        self.click(self.TO_PAYMENT_BUTTON)
        return self

    def get_full_name_error(self) -> str:
        """Retrieve full name validation error text."""
        return self.get_text(self.FULL_NAME_ERROR)

    def get_address_error(self) -> str:
        """Retrieve address line 1 validation error text."""
        return self.get_text(self.ADDRESS_1_ERROR)

    def get_city_error(self) -> str:
        """Retrieve city validation error text."""
        return self.get_text(self.CITY_ERROR)

    def get_zip_error(self) -> str:
        """Retrieve zip code validation error text."""
        return self.get_text(self.ZIP_ERROR)

    def get_country_error(self) -> str:
        """Retrieve country validation error text."""
        return self.get_text(self.COUNTRY_ERROR)

    def is_full_name_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Full Name input field is displayed."""
        return self.is_displayed(self.FULL_NAME_INPUT, timeout=timeout)

    def is_address_line_1_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Address Line 1 input field is displayed."""
        return self.is_displayed(self.ADDRESS_1_INPUT, timeout=timeout)

    def is_address_line_2_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Address Line 2 input field is displayed."""
        return self.is_displayed(self.ADDRESS_2_INPUT, timeout=timeout)

    def is_city_displayed(self, timeout: float = 3.0) -> bool:
        """Check if City input field is displayed."""
        return self.is_displayed(self.CITY_INPUT, timeout=timeout)

    def is_state_displayed(self, timeout: float = 3.0) -> bool:
        """Check if State/Region input field is displayed."""
        return self.is_displayed(self.STATE_INPUT, timeout=timeout)

    def is_zip_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Zip/Postal Code input field is displayed."""
        return self.is_displayed(self.ZIP_INPUT, timeout=timeout)

    def is_country_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Country input field is displayed."""
        return self.is_displayed(self.COUNTRY_INPUT, timeout=timeout)

    def is_to_payment_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if To Payment button is displayed."""
        return self.is_displayed(self.TO_PAYMENT_BUTTON, timeout=timeout)
