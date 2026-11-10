"""TC-076: Fill Valid Payment Information and Proceed to Order Review."""

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
@allure.story("Payment Information Submission")
@allure.title("TC-076: Fill Valid Payment Information and Proceed to Order Review")
@allure.issue("76")
def test_issue_076_fill_valid_payment_information_and_proceed_to_order_review(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
    checkout_review_page: CheckoutReviewPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Payment screen.

    Steps:
        1. Enter "Rebecca Winter" in Card Holder Name.
        2. Enter "325812657568789" in Card Number.
        3. Enter "03/25" in Expiration Date.
        4. Enter "123" in Security Code.
        5. Leave billing address checkbox checked.
        6. Tap "Review Order".

    Expected Result:
        - Payment details are accepted and user advances to Step 3 (Order Review screen).
    """
    with allure.step("Precondition: Complete shipping step and navigate to Payment screen"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        cart_page = CartPage(catalog_page.driver)
        cart_page.header.click_cart()
        cart_page.proceed_to_checkout()
        login_page = LoginPage(catalog_page.driver)
        login_page.login("bod@example.com", "10203040")
        assert checkout_shipping_page.is_loaded(), "Checkout Shipping address screen is not loaded"
        checkout_shipping_page.fill_shipping_details(
            full_name="Rebecca Winter",
            address_1="Mandara Way 89",
            city="Trujillo",
            zip_code="89112",
            country="United Kingdom",
        )
        checkout_shipping_page.proceed_to_payment()
        assert checkout_payment_page.is_loaded(), "Checkout Payment screen is not loaded"

    with allure.step("Step 1: Enter 'Rebecca Winter' in Card Holder Name"):
        checkout_payment_page.enter_card_holder_name("Rebecca Winter")

    with allure.step("Step 2: Enter '325812657568789' in Card Number"):
        checkout_payment_page.enter_card_number("325812657568789")

    with allure.step("Step 3: Enter '03/25' in Expiration Date"):
        checkout_payment_page.enter_expiration_date("03/25")

    with allure.step("Step 4: Enter '123' in Security Code"):
        checkout_payment_page.enter_security_code("123")

    with allure.step("Step 5: Leave billing address checkbox checked"):
        checkbox = checkout_payment_page.find_element(checkout_payment_page.BILLING_SAME_CHECKBOX)
        assert checkbox.get_attribute("checked") == "true", (
            "Billing address checkbox should be checked by default"
        )

    with allure.step("Step 6: Tap 'Review Order'"):
        checkout_payment_page.hide_keyboard()
        checkout_payment_page.proceed_to_review()

    with allure.step("Verify: Advances to Order Review screen"):
        assert checkout_review_page.is_loaded(), (
            "User did not advance to Step 3 (Checkout Review screen)"
        )
