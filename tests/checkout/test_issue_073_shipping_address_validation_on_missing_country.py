"""TC-073: Shipping Address Validation on Missing Country."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Shipping Address Validation")
@allure.title("TC-073: Shipping Address Validation on Missing Country")
@allure.issue("73")
def test_issue_073_shipping_address_validation_on_missing_country(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Shipping Address screen.

    Steps:
        1. Fill Full Name, Address Line 1, City, and Zip Code.
        2. Leave Country blank.
        3. Tap "To Payment".

    Expected Result:
        - An error message appears under Country: "Please provide your country.".
    """
    with allure.step("Precondition: Add product to cart, authenticate, and navigate to Shipping"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        cart_page = CartPage(catalog_page.driver)
        cart_page.header.click_cart()
        cart_page.proceed_to_checkout()
        login_page = LoginPage(catalog_page.driver)
        login_page.login("bod@example.com", "10203040")
        assert checkout_shipping_page.is_loaded(), "Checkout Shipping address screen is not loaded"

    with allure.step("Step 1: Fill Full Name, Address Line 1, City, and Zip Code"):
        checkout_shipping_page.enter_full_name("Rebecca Winter")
        checkout_shipping_page.enter_address_line_1("Mandara Way 89")
        checkout_shipping_page.enter_city("Trujillo")
        checkout_shipping_page.enter_zip("89112")

    with allure.step("Step 2: Leave Country blank"):
        pass

    with allure.step("Step 3: Tap 'To Payment'"):
        checkout_shipping_page.hide_keyboard()
        checkout_shipping_page.proceed_to_payment()

    with allure.step("Verify: Error message appears under Country"):
        country_error = checkout_shipping_page.get_country_error()
        assert country_error == "Please provide your country.", (
            f"Expected 'Please provide your country.', got '{country_error}'"
        )
