"""Test scenario for TC-054: Add Single Product to Shopping Cart."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Add To Cart")
@allure.title("TC-054: Add Single Product to Shopping Cart")
def test_issue_054_add_single_product_to_shopping_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        Shopping cart is empty; user is on the Product Details screen for "Sauce Labs Backpack".

    Steps:
        1. Tap the "Add to Cart" button.
        2. Check the cart icon in the top navigation bar.

    Expected Result:
        The product is added and the cart badge count updates to "1".
    """
    with allure.step(
        "Precondition: Shopping cart is empty; user is on Product Details for 'Sauce Labs Backpack'"
    ):
        assert catalog_page.get_cart_item_count() == 0, "Cart is not initially empty"
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"

    with allure.step("Step 1: Tap the 'Add to Cart' button"):
        product_details_page.add_to_cart()

    with allure.step("Step 2: Check the cart icon in the top navigation bar"):
        badge_count = product_details_page.header.get_cart_item_count()

    with allure.step("Expected Result: Cart badge count updates to '1'"):
        assert badge_count == 1, f"Expected cart badge count to update to 1, but got {badge_count}"
