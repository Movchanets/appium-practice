"""Test TC-061: Increase Item Quantity Directly Within the Cart."""

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
@allure.story("Quantity Management")
@allure.title("TC-061: Increase Item Quantity Directly Within the Cart")
@allure.issue("61")
def test_issue_061_increase_item_quantity_directly_within_the_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        Cart contains 1 item with quantity 1.
    Steps:
        1. Open the cart.
        2. Tap the plus (+) button on the item row.
    Expected Result:
        Item quantity updates to 2, and the total items count and price recalculate accordingly.
    """
    product_name = "Sauce Labs Backpack"

    with allure.step(f"Precondition: Add '{product_name}' to cart with quantity 1"):
        catalog_page.select_product_by_title(product_name)
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.add_to_cart()

    with allure.step("Step 1: Open the cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(catalog_page.driver)
        assert cart_page.is_loaded(), "Cart page did not load"
        cart_item = cart_page.get_cart_item_by_title(product_name)
        assert cart_item.get_quantity() == 1, "Initial item quantity is not 1"

    with allure.step("Step 2: Tap the plus (+) button on the item row"):
        cart_item.increase_quantity()

    with allure.step("Verify: Item quantity updates to 2, and total items and price recalculate"):
        assert cart_item.get_quantity() == 2, "Item quantity was not updated to 2"
        assert cart_page.get_total_items_count() == 2, "Total items count was not updated to 2"
        total_price = cart_page.get_total_price()
        assert "59.98" in total_price, (
            f"Expected total price to reflect 2 items ($59.98), got '{total_price}'"
        )
