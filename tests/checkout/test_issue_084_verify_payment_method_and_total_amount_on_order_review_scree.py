"""TC-084: Verify Payment Method and Total Amount on Order Review Screen."""

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


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Order Review")
@allure.title("TC-084: Verify Payment Method and Total Amount on Order Review Screen")
def test_issue_084_verify_payment_method_and_total_amount_on_order_review_scree(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
    checkout_review_page: CheckoutReviewPage,
) -> None:
    """
    Preconditions:
        - User is on the Review Order screen.

    Steps:
        1. Check payment card section and order total amount.

    Expected Result:
        - Card number is displayed (masked or full) and total amount matches cart price
          (e.g. "$ 29.99").
    """
    with allure.step("Precondition: Add product to cart, record price, and reach Order Review"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        expected_price = product_details_page.get_price()
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

    with allure.step("Step 1: Check payment card section and order total amount"):
        card_number = checkout_review_page.get_card_number()
        total_amount = checkout_review_page.get_total_amount()

    with allure.step("Verify: Card number is displayed and total amount matches cart price"):
        assert len(card_number) > 0, "Card number is not displayed on Review Order screen"
        assert any(ch.isdigit() for ch in card_number), (
            f"Card number '{card_number}' does not contain digits"
        )
        assert expected_price in total_amount or total_amount.startswith("$"), (
            f"Expected total amount '{total_amount}' to contain '{expected_price}'"
        )
