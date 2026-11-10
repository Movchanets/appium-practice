"""Test TC-063: Remove Product from Cart Using Remove Item Button."""

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
@allure.story("Item Removal")
@allure.title("TC-063: Remove Product from Cart Using Remove Item Button")
@allure.issue("63")
def test_issue_063_remove_product_from_cart_using_remove_item_button(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        Cart contains 1 item.
    Steps:
        1. Open the cart.
        2. Tap "Remove Item" on the product row.
    Expected Result:
        The product is removed from the list, and the cart switches to the empty state view.
    """
    product_name = "Sauce Labs Backpack"

    with allure.step(f"Precondition: Add '{product_name}' to cart"):
        catalog_page.select_product_by_title(product_name)
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.add_to_cart()

    with allure.step("Step 1: Open the cart"):
        product_details_page.header.click_cart()
        cart_page = CartPage(catalog_page.driver)
        assert cart_page.is_loaded(), "Cart page did not load"
        cart_item = cart_page.get_cart_item_by_title(product_name)

    with allure.step("Step 2: Tap 'Remove Item' on the product row"):
        cart_item.remove_item()

    with allure.step("Verify: Product is removed and cart switches to empty state view"):
        assert cart_page.is_empty(), "Cart did not switch to empty state view after removing item"
        assert cart_page.is_displayed(cart_page.NO_ITEMS_TITLE), (
            "No Items title is not displayed in empty cart"
        )
        assert cart_page.is_displayed(cart_page.GO_SHOPPING_BUTTON), (
            "Go Shopping button is not displayed in empty cart"
        )
