"""TC-088: Return to Catalog from Complete Screen and Verify Cart Reset."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_complete_page import CheckoutCompletePage
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
@allure.story("Order Confirmation")
@allure.title("TC-088: Return to Catalog from Complete Screen and Verify Cart Reset")
def test_issue_088_return_to_catalog_from_complete_screen_and_verify_cart_reset(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
    checkout_review_page: CheckoutReviewPage,
    checkout_complete_page: CheckoutCompletePage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Complete screen.

    Steps:
        1. Tap the "Continue Shopping" button.
        2. Observe the Catalog screen and header cart badge.

    Expected Result:
        - User is returned to the Catalog screen.
        - Shopping cart badge is reset to 0.
    """
    with allure.step("Precondition: User is on the Checkout Complete screen"):
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
        checkout_review_page.place_order()
        assert checkout_complete_page.is_loaded(), "Checkout Complete screen is not loaded"

    with allure.step("Step 1: Tap the 'Continue Shopping' button"):
        checkout_complete_page.click_continue_shopping()

    with allure.step("Step 2 & Verify: User is returned to Catalog and cart badge is reset to 0"):
        returned_catalog = CatalogPage(checkout_complete_page.driver)
        assert returned_catalog.is_loaded(), "User was not returned to Catalog screen"
        cart_count = returned_catalog.get_cart_item_count()
        assert cart_count == 0, f"Expected cart badge count to be 0, but got {cart_count}"
