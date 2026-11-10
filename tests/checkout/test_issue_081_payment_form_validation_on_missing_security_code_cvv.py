"""TC-081: Payment Form Validation on Missing Security Code CVV."""

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
@allure.story("Payment Method Validation")
@allure.title("TC-081: Payment Form Validation on Missing Security Code CVV")
def test_issue_081_payment_form_validation_on_missing_security_code_cvv(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Payment screen.

    Steps:
        1. Fill Card Holder Name, Card Number, and Expiration Date.
        2. Leave Security Code blank.
        3. Tap "Review Order".

    Expected Result:
        - An error message appears under Security Code: "Please provide your security code.".
    """
    with allure.step("Precondition: Add product to cart, authenticate, and navigate to Payment"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        cart_page = CartPage(catalog_page.driver)
        cart_page.header.click_cart()
        cart_page.proceed_to_checkout()
        login_page = LoginPage(catalog_page.driver)
        if login_page.is_displayed(login_page.USERNAME_INPUT, timeout=3.0):
            login_page.login("bod@example.com", "10203040")
        assert checkout_shipping_page.is_loaded(), "Checkout Shipping address screen is not loaded"
        checkout_shipping_page.fill_shipping_details(
            full_name="Rebecca Winter",
            address_1="Mandore Laboratory",
            city="Truro",
            state="Cornwall",
            zip_code="89101",
            country="United Kingdom",
        )
        checkout_shipping_page.proceed_to_payment()
        assert checkout_payment_page.is_loaded(), "Checkout Payment screen is not loaded"

    with allure.step("Step 1: Fill Card Holder Name, Card Number, and Expiration Date"):
        checkout_payment_page.enter_card_holder_name("Rebecca Winter")
        checkout_payment_page.enter_card_number("325812657568789")
        checkout_payment_page.enter_expiration_date("03/25")

    with allure.step("Step 2: Leave Security Code blank"):
        pass

    with allure.step("Step 3: Tap 'Review Order'"):
        checkout_payment_page.hide_keyboard()
        checkout_payment_page.proceed_to_review()

    with allure.step("Verify: Error message appears under Security Code"):
        assert checkout_payment_page.is_displayed(checkout_payment_page.SECURITY_CODE_ERROR), (
            "Security code error element is not displayed"
        )
        security_code_error = checkout_payment_page.get_security_code_error()
        assert security_code_error == "Please provide your security code.", (
            f"Expected 'Please provide your security code.', got '{security_code_error}'"
        )
