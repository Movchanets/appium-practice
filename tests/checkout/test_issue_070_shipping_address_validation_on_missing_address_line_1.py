"""Test TC-070: Shipping Address Validation on Missing Address Line 1."""

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
@allure.title("TC-070: Shipping Address Validation on Missing Address Line 1")
@allure.issue("70")
def test_issue_070_shipping_address_validation_on_missing_address_line_1(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        User is on the Checkout Shipping Address screen.
    Steps:
        1. Fill Full Name.
        2. Leave Address Line 1 blank.
        3. Fill remaining fields and tap "To Payment".
    Expected Result:
        An error message appears under Address Line 1: "Please provide your address.".
    """
    try:
        with allure.step("Precondition: User is on Checkout Shipping Address screen"):
            catalog_page.navigate_to_login()
            login_page = LoginPage(catalog_page.driver)
            assert login_page.is_loaded(), "Login page did not load"
            login_page.login("bod@example.com", "10203040")

            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
            assert catalog_page.is_loaded(), "Catalog page did not load"
            catalog_page.select_product_by_title("Sauce Labs Backpack")
            assert product_details_page.is_loaded(), "Product details page did not load"
            product_details_page.add_to_cart()
            product_details_page.header.click_cart()

            cart_page = CartPage(catalog_page.driver)
            assert cart_page.is_loaded(), "Cart page did not load"
            cart_page.proceed_to_checkout()
            assert checkout_shipping_page.is_loaded(), "Shipping Address screen did not load"

        with allure.step("Step 1: Fill Full Name"):
            checkout_shipping_page.enter_full_name("Rebecca Winter")

        with allure.step("Step 2: Leave Address Line 1 blank"):
            pass  # Address Line 1 is initially empty

        with allure.step("Step 3: Fill remaining fields and tap 'To Payment'"):
            checkout_shipping_page.enter_city("Truro")
            checkout_shipping_page.enter_state("Cornwall")
            checkout_shipping_page.enter_zip("89101")
            checkout_shipping_page.enter_country("United Kingdom")
            checkout_shipping_page.hide_keyboard()
            checkout_shipping_page.proceed_to_payment()

        with allure.step("Verify: Error message appears under Address Line 1"):
            assert checkout_shipping_page.is_loaded(), (
                "Form was submitted despite missing Address Line 1"
            )
            error_message = checkout_shipping_page.get_address_error()
            assert error_message == "Please provide your address.", (
                f"Expected 'Please provide your address.', got '{error_message}'"
            )
    finally:
        with allure.step("Teardown: Log out if logged in"):
            try:
                checkout_shipping_page.open_menu()
                checkout_shipping_page.drawer_menu.logout_if_logged_in()
            except Exception:
                pass
