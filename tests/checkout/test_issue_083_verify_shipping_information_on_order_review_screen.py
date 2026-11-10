"""TC-083: Verify Shipping Information on Order Review Screen."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_review_page import CheckoutReviewPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Order Review")
@allure.title("TC-083: Verify Shipping Information on Order Review Screen")
@allure.issue("83")
def test_issue_083_verify_shipping_information_on_order_review_screen(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
    checkout_review_page: CheckoutReviewPage,
) -> None:
    """
    Preconditions:
        - User has completed Steps 1 & 2 with recipient "Rebecca Winter"
          and address "Mandore Laboratory".

    Steps:
        1. Observe the Review Order screen.

    Expected Result:
        - Shipping address section correctly displays recipient name "Rebecca Winter"
          and street address "Mandore Laboratory".
    """
    with allure.step("Precondition: Complete Steps 1 & 2 to reach Order Review"):
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
        checkout_payment_page.fill_payment_details(
            name="Rebecca Winter",
            card_number="325812657568789",
            expiration_date="03/25",
            security_code="123",
            billing_same=True,
        )
        checkout_payment_page.proceed_to_review()
        assert checkout_review_page.is_loaded(), "Order Review screen is not loaded"

    with allure.step("Step 1: Observe the Review Order screen"):
        pass

    with allure.step("Verify: Shipping address displays recipient name and street address"):
        shipping_name = checkout_review_page.get_shipping_name()
        assert shipping_name == "Rebecca Winter", (
            f"Expected shipping name 'Rebecca Winter', got '{shipping_name}'"
        )
        shipping_address = checkout_review_page.get_shipping_address()
        assert shipping_address == "Mandore Laboratory", (
            f"Expected shipping address 'Mandore Laboratory', got '{shipping_address}'"
        )
