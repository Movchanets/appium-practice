"""TC-075: Verify Checkout Payment Screen Layout and Default Billing Checkbox."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Payment Screen Layout")
@allure.title("TC-075: Verify Checkout Payment Screen Layout and Default Billing Checkbox")
def test_issue_075_verify_checkout_payment_screen_layout_and_default_billing_ch(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        - User has completed Step 1 and reached the Payment Method screen.

    Steps:
        1. Observe the Checkout Payment screen.

    Expected Result:
        - Screen displays fields for Card Holder Name, Card Number, Expiration Date,
          Security Code, and the checkbox "My billing address is the same as my
          shipping address" is checked by default.
    """
    with allure.step("Precondition: Complete shipping step and navigate to Payment screen"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        cart_page = CartPage(catalog_page.driver)
        cart_page.header.click_cart()
        cart_page.proceed_to_checkout()
        login_page = LoginPage(catalog_page.driver)
        login_page.login("bod@example.com", "10203040")
        assert checkout_shipping_page.is_loaded(), "Checkout Shipping address screen is not loaded"
        checkout_shipping_page.fill_shipping_details(
            full_name="Rebecca Winter",
            address_1="Mandara Way 89",
            city="Trujillo",
            zip_code="89112",
            country="United Kingdom",
        )
        checkout_shipping_page.proceed_to_payment()
        assert checkout_payment_page.is_loaded(), "Checkout Payment screen is not loaded"

    with allure.step("Step 1: Observe the Checkout Payment screen layout"):
        assert checkout_payment_page.is_displayed(checkout_payment_page.NAME_INPUT), (
            "Card Holder Name input field is not displayed"
        )
        assert checkout_payment_page.is_displayed(checkout_payment_page.CARD_NUMBER_INPUT), (
            "Card Number input field is not displayed"
        )
        assert checkout_payment_page.is_displayed(checkout_payment_page.EXPIRATION_DATE_INPUT), (
            "Expiration Date input field is not displayed"
        )
        assert checkout_payment_page.is_displayed(checkout_payment_page.SECURITY_CODE_INPUT), (
            "Security Code input field is not displayed"
        )
        assert checkout_payment_page.is_displayed(checkout_payment_page.BILLING_SAME_CHECKBOX), (
            "Billing address checkbox is not displayed"
        )

    with allure.step("Verify: Billing address checkbox is checked by default"):
        checkbox = checkout_payment_page.find_element(checkout_payment_page.BILLING_SAME_CHECKBOX)
        assert checkbox.get_attribute("checked") == "true", (
            "Billing address checkbox is not checked by default"
        )
