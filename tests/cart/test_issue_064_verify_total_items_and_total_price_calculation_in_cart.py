"""Test TC-064: Verify Total Items and Total Price Calculation in Cart."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Summary Calculation")
@allure.title("TC-064: Verify Total Items and Total Price Calculation in Cart")
@allure.issue("64")
def test_issue_064_verify_total_items_and_total_price_calculation_in_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        Cart contains "Sauce Labs Backpack" ($29.99) and "Sauce Labs Bike Light" ($9.99).
    Steps:
        1. Open the cart.
        2. Check the summary section at the bottom of the cart.
    Expected Result:
        Total items count displays "2 Items" and total price displays "$ 39.98".
    """
    with allure.step("Precondition: Add 'Sauce Labs Backpack' ($29.99) to cart"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.add_to_cart()

    with allure.step("Precondition: Return to catalog and add 'Sauce Labs Bike Light' to cart"):
        product_details_page.open_menu()
        product_details_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page did not load"
        catalog_page.select_product_by_title("Sauce Labs Bike Light")
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.add_to_cart()

    with allure.step("Step 1: Open the cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(catalog_page.driver)
        assert cart_page.is_loaded(), "Cart page did not load"

    with allure.step("Step 2: Check the summary section at the bottom of the cart"):
        items_count = cart_page.get_total_items_count()
        total_items_text = cart_page.get_text(cart_page.TOTAL_ITEMS_LABEL)
        total_price = cart_page.get_total_price()

    with allure.step("Verify: Total items is 2 and total price displays '$ 39.98'"):
        assert items_count == 2, f"Expected 2 items, got {items_count}"
        assert "2" in total_items_text and "Item" in total_items_text, (
            f"Expected '2 Items' in items label, got '{total_items_text}'"
        )
        assert "39.98" in total_price, (
            f"Expected total price to contain '39.98', got '{total_price}'"
        )
