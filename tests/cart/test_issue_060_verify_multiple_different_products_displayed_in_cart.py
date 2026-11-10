"""Test scenario for TC-060: Verify Multiple Different Products Displayed in Cart."""

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
@allure.story("Multiple Products Display")
@allure.title("TC-060: Verify Multiple Different Products Displayed in Cart")
@allure.issue("60")
def test_issue_060_verify_multiple_different_products_displayed_in_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        Added "Sauce Labs Backpack" and "Sauce Labs Bike Light" to the cart.

    Steps:
        1. Open the shopping cart.

    Expected Result:
        Both products are displayed in separate item rows with their respective details.
    """
    with allure.step(
        "Precondition: Add 'Sauce Labs Backpack' and 'Sauce Labs Bike Light' to the cart"
    ):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page failed to load for Backpack"
        product_details_page.add_to_cart()
        assert product_details_page.header.get_cart_item_count() == 1, (
            "Cart count did not update to 1 after adding Backpack"
        )

        product_details_page.open_menu()
        product_details_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Failed to return to Catalog page"

        catalog_page.select_product_by_title("Sauce Labs Bike Light")
        assert product_details_page.is_loaded(), (
            "Product details page failed to load for Bike Light"
        )
        product_details_page.add_to_cart()
        assert product_details_page.header.get_cart_item_count() == 2, (
            "Cart count did not update to 2 after adding Bike Light"
        )

    with allure.step("Step 1: Open the shopping cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(product_details_page.driver)
        assert cart_page.is_loaded(), "Cart screen did not load"

    with allure.step(
        "Expected Result: Both products are displayed in separate item rows"
        " with their respective details"
    ):
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) >= 2, (
            f"Expected at least 2 cart item rows, but got {len(cart_items)}"
        )
        backpack_item = cart_page.get_cart_item_by_title("Sauce Labs Backpack")
        bike_light_item = cart_page.get_cart_item_by_title("Sauce Labs Bike Light")

        assert "Sauce Labs Backpack" in backpack_item.get_title(), (
            f"Expected title 'Sauce Labs Backpack', got '{backpack_item.get_title()}'"
        )
        assert "Sauce Labs Bike Light" in bike_light_item.get_title(), (
            f"Expected title 'Sauce Labs Bike Light', got '{bike_light_item.get_title()}'"
        )
        assert backpack_item.get_quantity() >= 1, (
            f"Expected Backpack quantity >= 1, got {backpack_item.get_quantity()}"
        )
        assert bike_light_item.get_quantity() >= 1, (
            f"Expected Bike Light quantity >= 1, got {bike_light_item.get_quantity()}"
        )
