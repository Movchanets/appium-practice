"""TC-074: Dismiss Soft Keyboard to Access To Payment Button."""

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
@allure.story("Soft Keyboard Navigation")
@allure.title("TC-074: Dismiss Soft Keyboard to Access To Payment Button")
@allure.issue("74")
def test_issue_074_dismiss_soft_keyboard_to_access_to_payment_button(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Shipping Address screen with soft keyboard visible.

    Steps:
        1. Tap outside the input fields or press the Back button to dismiss the keyboard.
        2. Scroll down if necessary to view the bottom of the form.

    Expected Result:
        - Soft keyboard closes cleanly without clearing input fields, leaving
          the "To Payment" button fully visible and clickable.
    """
    with allure.step("Precondition: User is on Shipping screen with keyboard open"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        cart_page = CartPage(catalog_page.driver)
        cart_page.header.click_cart()
        cart_page.proceed_to_checkout()
        login_page = LoginPage(catalog_page.driver)
        login_page.login("bod@example.com", "10203040")
        assert checkout_shipping_page.is_loaded(), "Checkout Shipping address screen is not loaded"
        checkout_shipping_page.enter_full_name("Rebecca Winter")

    with allure.step("Step 1: Tap outside the input fields or dismiss the keyboard"):
        checkout_shipping_page.hide_keyboard()

    with allure.step("Step 2: Scroll down if necessary to view the bottom of the form"):
        to_payment_btn = checkout_shipping_page.TO_PAYMENT_BUTTON
        if not checkout_shipping_page.is_displayed(to_payment_btn, timeout=2.0):
            checkout_shipping_page.swipe_up()

    with allure.step("Verify: Soft keyboard closed without clearing fields, and button visible"):
        entered_name = checkout_shipping_page.get_text(checkout_shipping_page.FULL_NAME_INPUT)
        assert entered_name == "Rebecca Winter", (
            f"Input field cleared unexpectedly: expected 'Rebecca Winter', got '{entered_name}'"
        )
        assert checkout_shipping_page.is_displayed(checkout_shipping_page.TO_PAYMENT_BUTTON), (
            "'To Payment' button is not displayed and clickable"
        )
