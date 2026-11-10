"""Test TC-062: Decrease Item Quantity Directly Within the Cart."""

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
@allure.title("TC-062: Decrease Item Quantity Directly Within the Cart")
def test_issue_062_decrease_item_quantity_directly_within_the_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        Cart contains an item with quantity 2.
    Steps:
        1. Open the cart.
        2. Tap the minus (-) button on the item row.
    Expected Result:
        Item quantity decrements to 1, and the total price updates.
    """
    product_name = "Sauce Labs Backpack"

    with allure.step(f"Precondition: Add '{product_name}' to cart with quantity 2"):
        catalog_page.select_product_by_title(product_name)
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.increase_quantity(1)
        assert product_details_page.get_quantity() == 2, "Product quantity is not 2 on details page"
        product_details_page.add_to_cart()

    with allure.step("Step 1: Open the cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(catalog_page.driver)
        assert cart_page.is_loaded(), "Cart page did not load"
        cart_item = cart_page.get_cart_item_by_title(product_name)
        assert cart_item.get_quantity() == 2, "Initial cart item quantity is not 2"

    with allure.step("Step 2: Tap the minus (-) button on the item row"):
        cart_item.decrease_quantity()

    with allure.step("Verify: Item quantity decrements to 1, and the total price updates"):
        assert cart_item.get_quantity() == 1, "Item quantity was not decremented to 1"
        assert cart_page.get_total_items_count() == 1, "Total items count was not updated to 1"
        total_price = cart_page.get_total_price()
        assert "29.99" in total_price, (
            f"Expected total price to contain '29.99', got '{total_price}'"
        )
