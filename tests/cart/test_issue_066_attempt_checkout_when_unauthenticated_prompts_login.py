"""Test TC-066: Attempt Checkout when Unauthenticated Prompts Login."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Checkout Authentication")
@allure.title("TC-066: Attempt Checkout when Unauthenticated Prompts Login")
@allure.issue("66")
def test_issue_066_attempt_checkout_when_unauthenticated_prompts_login(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        User is not logged in (guest) and has an item in the cart.
    Steps:
        1. Open the cart.
        2. Tap "Proceed To Checkout".
    Expected Result:
        User is redirected to the Login screen with an indication to sign in before
        proceeding with checkout.
    """
    with allure.step("Precondition: Ensure user is logged out and add 1 item to cart"):
        catalog_page.logout_if_logged_in()
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

    with allure.step("Verify: User is redirected to Login screen"):
        login_page = LoginPage(cart_page.driver)
        assert login_page.is_loaded(), "Login screen was not displayed upon checkout attempt"
        assert login_page.is_displayed(login_page.TITLE), "Login title is not visible"
        assert login_page.get_text(login_page.TITLE) == "Login", (
            f"Expected title 'Login', got '{login_page.get_text(login_page.TITLE)}'"
        )
