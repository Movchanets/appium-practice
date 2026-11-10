"""TC-080: Payment Form Validation on Missing Expiration Date."""

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
@allure.feature("Checkout")
@allure.story("Payment Form Validation")
@allure.title("TC-080: Payment Form Validation on Missing Expiration Date")
@allure.issue("80")
def test_issue_080_payment_form_validation_on_missing_expiration_date(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Payment screen.

    Steps:
        1. Fill Card Holder Name and Card Number.
        2. Leave Expiration Date blank.
        3. Fill CVV and tap "Review Order".

    Expected Result:
        - An error message appears under Expiration Date: "Please provide your expiration date.".
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

    with allure.step("Step 1: Fill Card Holder Name and Card Number"):
        checkout_payment_page.enter_card_holder_name("Rebecca Winter")
        checkout_payment_page.enter_card_number("325812657568789")

    with allure.step("Step 2: Leave Expiration Date blank"):
        pass

    with allure.step("Step 3: Fill CVV and tap 'Review Order'"):
        checkout_payment_page.enter_security_code("123")
        checkout_payment_page.hide_keyboard()
        checkout_payment_page.proceed_to_review()

    with allure.step("Verify: Error message appears under Expiration Date"):
        exp_date_error = checkout_payment_page.get_expiration_date_error()
        assert exp_date_error == "Please provide your expiration date.", (
            f"Expected 'Please provide your expiration date.', got '{exp_date_error}'"
        )
