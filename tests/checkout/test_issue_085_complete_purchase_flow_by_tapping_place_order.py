"""TC-085: Complete Purchase Flow by Tapping Place Order."""

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


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Order Submission")
@allure.title("TC-085: Complete Purchase Flow by Tapping Place Order")
def test_issue_085_complete_purchase_flow_by_tapping_place_order(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
    checkout_review_page: CheckoutReviewPage,
    checkout_complete_page: CheckoutCompletePage,
) -> None:
    """
    Preconditions:
        - User is on the Review Order screen with verified details.

    Steps:
        1. Tap the "Place Order" button.

    Expected Result:
        - Order is processed and user is redirected to the Checkout Complete screen.
    """
    with allure.step("Precondition: User is on the Review Order screen with verified details"):
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

    with allure.step("Step 1: Tap the 'Place Order' button"):
        checkout_review_page.place_order()

    with allure.step("Verify: Order is processed and user redirected to Checkout Complete"):
        assert checkout_complete_page.is_loaded(), (
            "User was not redirected to Checkout Complete screen"
        )
