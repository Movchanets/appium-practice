"""TC-079: Payment Form Validation on Missing Card Number."""

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
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.checkout
@pytest.mark.xfail(
    reason=(
        "BUG: AUT lacks cardNumberErrorTV; only cardNumberErrorIV icon is displayed "
        "without error text for missing card number"
    ),
    strict=False,
)
@allure.feature("Checkout")
@allure.story("Payment Form Validation")
@allure.title("TC-079: Payment Form Validation on Missing Card Number")
@allure.issue("79")
def test_issue_079_payment_form_validation_on_missing_card_number(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Payment screen.

    Steps:
        1. Fill Card Holder Name.
        2. Leave Card Number blank.
        3. Fill Expiration Date and CVV, then tap "Review Order".

    Expected Result:
        - An error message appears under Card Number: "Please provide your card number.".
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

    with allure.step("Step 1: Fill Card Holder Name"):
        checkout_payment_page.enter_card_holder_name("Rebecca Winter")

    with allure.step("Step 2: Leave Card Number blank"):
        checkout_payment_page.clear_card_number()

    with allure.step("Step 3: Fill Expiration Date and CVV, then tap 'Review Order'"):
        checkout_payment_page.enter_expiration_date("03/25")
        checkout_payment_page.enter_security_code("123")
        checkout_payment_page.hide_keyboard()
        checkout_payment_page.proceed_to_review()

    with allure.step("Verify: Error message appears under Card Number"):
        card_number_error = checkout_payment_page.get_card_number_error()
        assert card_number_error == "Please provide your card number.", (
            f"Expected 'Please provide your card number.', got '{card_number_error}'"
        )
