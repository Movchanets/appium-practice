"""TC-077: Toggle Same Billing Address as Shipping Address Checkbox."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Billing Address Checkbox")
@allure.title("TC-077: Toggle Same Billing Address as Shipping Address Checkbox")
def test_issue_077_toggle_same_billing_address_as_shipping_address_checkbox(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        - User is on the Checkout Payment screen.

    Steps:
        1. Tap the billing address checkbox to uncheck it.
        2. Verify it becomes unchecked.
        3. Tap the checkbox again to check it.

    Expected Result:
        - The checkbox toggles smoothly between checked and unchecked states.
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

    with allure.step("Step 1: Tap the billing address checkbox to uncheck it"):
        checkbox = checkout_payment_page.find_element(checkout_payment_page.BILLING_SAME_CHECKBOX)
        assert checkbox.get_attribute("checked") == "true", (
            "Billing address checkbox should be checked initially"
        )
        checkbox.click()

    with allure.step("Step 2: Verify it becomes unchecked"):
        assert checkbox.get_attribute("checked") == "false", (
            "Billing address checkbox failed to uncheck after tap"
        )

    with allure.step("Step 3: Tap the checkbox again to check it"):
        checkbox.click()

    with allure.step("Verify: Checkbox returns to checked state"):
        assert checkbox.get_attribute("checked") == "true", (
            "Billing address checkbox failed to re-check after second tap"
        )
