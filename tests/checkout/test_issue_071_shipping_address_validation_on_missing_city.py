"""TC-071: Shipping Address Validation on Missing City."""

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
@allure.title("TC-071: Shipping Address Validation on Missing City")
def test_issue_071_shipping_address_validation_on_missing_city(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Shipping Address screen.

    Steps:
        1. Fill Full Name and Address Line 1.
        2. Leave City blank.
        3. Fill Zip Code and Country, then tap "To Payment".

    Expected Result:
        - An error message appears under City: "Please provide your city.".
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

    with allure.step("Step 1: Fill Full Name and Address Line 1"):
        checkout_shipping_page.enter_full_name("Rebecca Winter")
        checkout_shipping_page.enter_address_line_1("Mandara Way 89")

    with allure.step("Step 2: Leave City blank"):
        pass

    with allure.step("Step 3: Fill Zip Code and Country, then tap 'To Payment'"):
        checkout_shipping_page.enter_zip("89112")
        checkout_shipping_page.enter_country("United Kingdom")
        checkout_shipping_page.hide_keyboard()
        checkout_shipping_page.proceed_to_payment()

    with allure.step("Verify: Error message appears under City"):
        city_error = checkout_shipping_page.get_city_error()
        assert city_error == "Please provide your city.", (
            f"Expected 'Please provide your city.', got '{city_error}'"
        )
