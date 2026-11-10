"""Test TC-068: Fill Valid Shipping Address and Proceed to Payment."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.checkout
@allure.feature("Checkout")
@allure.story("Shipping Address Entry")
@allure.title("TC-068: Fill Valid Shipping Address and Proceed to Payment")
def test_issue_068_fill_valid_shipping_address_and_proceed_to_payment(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    checkout_shipping_page: CheckoutShippingPage,
    checkout_payment_page: CheckoutPaymentPage,
) -> None:
    """
    Preconditions:
        User is on the Checkout Shipping Address screen.
    Steps:
        1. Enter "Rebecca Winter" in Full Name.
        2. Enter "Mandore Laboratory" in Address Line 1.
        3. Enter "Truro" in City.
        4. Enter "Cornwall" in State/Region.
        5. Enter "89101" in Zip Code.
        6. Enter "United Kingdom" in Country.
        7. Tap "To Payment".
    Expected Result:
        Shipping address is accepted and user advances to Step 2 (Checkout Payment screen).
    """
    try:
        with allure.step("Precondition: User navigates to Checkout Shipping screen"):
            catalog_page.navigate_to_login()
            login_page = LoginPage(catalog_page.driver)
            assert login_page.is_loaded(), "Login page did not load"
            login_page.login("bod@example.com", "10203040")

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
            assert checkout_shipping_page.is_loaded(), "Shipping Address screen did not load"

        with allure.step("Step 1: Enter 'Rebecca Winter' in Full Name"):
            checkout_shipping_page.enter_full_name("Rebecca Winter")

        with allure.step("Step 2: Enter 'Mandore Laboratory' in Address Line 1"):
            checkout_shipping_page.enter_address_line_1("Mandore Laboratory")

        with allure.step("Step 3: Enter 'Truro' in City"):
            checkout_shipping_page.enter_city("Truro")

        with allure.step("Step 4: Enter 'Cornwall' in State/Region"):
            checkout_shipping_page.enter_state("Cornwall")

        with allure.step("Step 5: Enter '89101' in Zip Code"):
            checkout_shipping_page.enter_zip("89101")

        with allure.step("Step 6: Enter 'United Kingdom' in Country"):
            checkout_shipping_page.enter_country("United Kingdom")
            checkout_shipping_page.hide_keyboard()

        with allure.step("Step 7: Tap 'To Payment'"):
            checkout_shipping_page.proceed_to_payment()

        with allure.step("Verify: Shipping address accepted and user advances to Payment screen"):
            assert checkout_payment_page.is_loaded(), "Checkout Payment screen was not displayed"
            assert checkout_payment_page.get_text(checkout_payment_page.TITLE) == "Checkout"
            assert (
                checkout_payment_page.get_text(checkout_payment_page.SUBTITLE)
                == "Enter a payment method"
            )
    finally:
        with allure.step("Teardown: Log out if logged in"):
            try:
                checkout_shipping_page.open_menu()
                checkout_shipping_page.drawer_menu.logout_if_logged_in()
            except Exception:
                pass
