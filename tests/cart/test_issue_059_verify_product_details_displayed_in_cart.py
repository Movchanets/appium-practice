"""Test scenario for TC-059: Verify Product Details Displayed in Cart."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Cart Item Details")
@allure.title("TC-059: Verify Product Details Displayed in Cart")
@allure.issue("59")
def test_issue_059_verify_product_details_displayed_in_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        One "Sauce Labs Backpack" has been added to the cart.

    Steps:
        1. Open the shopping cart.
        2. Inspect the item row in the list.

    Expected Result:
        The cart row shows product title ("Sauce Labs Backpack"), price ("$ 29.99"),
        thumbnail, selected color, and quantity 1.
    """
    with allure.step("Precondition: One 'Sauce Labs Backpack' has been added to the cart"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.add_to_cart()
        assert product_details_page.header.get_cart_item_count() == 1, (
            "Cart badge count did not update to 1 after adding product"
        )

    with allure.step("Step 1: Open the shopping cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(product_details_page.driver)
        assert cart_page.is_loaded(), "Cart screen did not load"

    with allure.step("Step 2 & Expected Result: Inspect the item row in the list"):
        cart_item = cart_page.get_cart_item_by_title("Sauce Labs Backpack")
        assert "Sauce Labs Backpack" in cart_item.get_title(), (
            f"Expected product title 'Sauce Labs Backpack', but got '{cart_item.get_title()}'"
        )
        assert "$ 29.99" in cart_item.get_price(), (
            f"Expected product price '$ 29.99', but got '{cart_item.get_price()}'"
        )
        assert cart_item.get_quantity() == 1, (
            f"Expected item quantity 1, but got {cart_item.get_quantity()}"
        )
        assert cart_item.is_displayed(cart_item.IMAGE), "Product thumbnail image is not displayed"
        assert cart_item.is_displayed(cart_item.COLOR_ICON) or cart_item.is_displayed(
            cart_item.COLOR_LABEL
        ), "Product selected color is not displayed"
