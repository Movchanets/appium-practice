"""Test TC-067: Verify Checkout Shipping Address Screen Layout."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Shipping Address Screen")
@allure.title("TC-067: Verify Checkout Shipping Address Screen Layout")
@allure.issue("67")
def test_issue_067_verify_checkout_shipping_address_screen_layout(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        User is logged in and taps Proceed to Checkout from cart.
    Steps:
        1. Observe the Checkout Shipping Address screen.
    Expected Result:
        Screen displays title "Checkout", subtitle "Enter a shipping address",
        input fields for Full Name, Address Lines 1 & 2, City, State/Region,
        Zip Code, Country, and a "To Payment" button.
    """
    try:
        with allure.step("Precondition: User logs in with valid credentials"):
            catalog_page.navigate_to_login()
            login_page = LoginPage(catalog_page.driver)
            assert login_page.is_loaded(), "Login page did not load"
            login_page.login("bod@example.com", "10203040")

        with allure.step("Precondition: Add item to cart and proceed to checkout"):
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

        with allure.step("Step 1: Observe the Checkout Shipping Address screen"):
            assert checkout_shipping_page.is_loaded(), (
                "Checkout Shipping Address screen is not loaded"
            )

        with allure.step("Verify: Screen layout displays all required fields"):
            actual_title = checkout_shipping_page.get_text(checkout_shipping_page.TITLE)
            assert actual_title == "Checkout", f"Expected title 'Checkout', got '{actual_title}'"

            actual_subtitle = checkout_shipping_page.get_text(checkout_shipping_page.SUBTITLE)
            assert actual_subtitle == "Enter a shipping address", (
                f"Expected subtitle 'Enter a shipping address', got '{actual_subtitle}'"
            )

            assert checkout_shipping_page.is_displayed(checkout_shipping_page.FULL_NAME_INPUT), (
                "Full Name input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.ADDRESS_1_INPUT), (
                "Address Line 1 input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.ADDRESS_2_INPUT), (
                "Address Line 2 input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.CITY_INPUT), (
                "City input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.STATE_INPUT), (
                "State/Region input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.ZIP_INPUT), (
                "Zip Code input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.COUNTRY_INPUT), (
                "Country input is not displayed"
            )
            assert checkout_shipping_page.is_displayed(checkout_shipping_page.TO_PAYMENT_BUTTON), (
                "To Payment button is not displayed"
            )
    finally:
        with allure.step("Teardown: Log out if logged in"):
            try:
                checkout_shipping_page.open_menu()
                checkout_shipping_page.drawer_menu.logout_if_logged_in()
            except Exception:
                pass
