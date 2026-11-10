"""Test TC-069: Shipping Address Validation on Missing Full Name."""

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
@allure.title("TC-069: Shipping Address Validation on Missing Full Name")
@allure.issue("69")
def test_issue_069_shipping_address_validation_on_missing_full_name(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        User is on the Checkout Shipping Address screen.
    Steps:
        1. Leave Full Name blank.
        2. Fill Address 1, City, Zip Code, and Country with valid data.
        3. Tap "To Payment".
    Expected Result:
        Form submission is blocked and an error message appears under Full Name:
        "Please provide your full name.".
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

        with allure.step("Step 1: Leave Full Name blank"):
            pass  # Full Name input is initially empty

        with allure.step("Step 2: Fill Address 1, City, Zip Code, and Country with valid data"):
            checkout_shipping_page.enter_address_line_1("Mandore Laboratory")
            checkout_shipping_page.enter_city("Truro")
            checkout_shipping_page.enter_state("Cornwall")
            checkout_shipping_page.enter_zip("89101")
            checkout_shipping_page.enter_country("United Kingdom")
            checkout_shipping_page.hide_keyboard()

        with allure.step("Step 3: Tap 'To Payment'"):
            checkout_shipping_page.proceed_to_payment()

        with allure.step("Verify: Form submission is blocked and error appears under Full Name"):
            assert checkout_shipping_page.is_loaded(), (
                "Form was submitted despite missing Full Name"
            )
            error_message = checkout_shipping_page.get_full_name_error()
            assert error_message == "Please provide your full name.", (
                f"Expected 'Please provide your full name.', got '{error_message}'"
            )
    finally:
        with allure.step("Teardown: Log out if logged in"):
            try:
                checkout_shipping_page.open_menu()
                checkout_shipping_page.drawer_menu.logout_if_logged_in()
            except Exception:
                pass
