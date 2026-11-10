"""Test TC-065: Proceed to Checkout when User is Logged In."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Checkout Progression")
@allure.title("TC-065: Proceed to Checkout when User is Logged In")
def test_issue_065_proceed_to_checkout_when_user_is_logged_in(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        User is logged in and has at least one item in the cart.
    Steps:
        1. Open the cart.
        2. Tap "Proceed To Checkout".
    Expected Result:
        User advances directly to Step 1 of Checkout (Shipping Address screen).
    """
    try:
        with allure.step("Precondition: User logs in with valid credentials"):
            catalog_page.navigate_to_login()
            login_page = LoginPage(catalog_page.driver)
            assert login_page.is_loaded(), "Login page did not load"
            login_page.login("bod@example.com", "10203040")

        with allure.step("Precondition: Navigate to catalog and add 1 item to cart"):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
            assert catalog_page.is_loaded(), "Catalog page did not load"
            catalog_page.select_product_by_title("Sauce Labs Backpack")
            assert product_details_page.is_loaded(), "Product details page did not load"
            product_details_page.add_to_cart()

        with allure.step("Step 1: Open the cart"):
            product_details_page.header.click_cart()
            cart_page = CartPage(catalog_page.driver)
            assert cart_page.is_loaded(), "Cart page did not load"

        with allure.step("Step 2: Tap 'Proceed To Checkout'"):
            cart_page.proceed_to_checkout()

        with allure.step("Verify: User advances directly to Step 1 of Checkout"):
            assert checkout_shipping_page.is_loaded(), (
                "Checkout Shipping Address screen was not displayed"
            )
            assert checkout_shipping_page.get_text(checkout_shipping_page.TITLE) == "Checkout"
            assert (
                checkout_shipping_page.get_text(checkout_shipping_page.SUBTITLE)
                == "Enter a shipping address"
            )
    finally:
        with allure.step("Teardown: Log out if logged in"):
            try:
                checkout_shipping_page.open_menu()
                checkout_shipping_page.drawer_menu.logout_if_logged_in()
            except Exception:
                pass
