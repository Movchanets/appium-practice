"""Test scenario for TC-057: Verify Empty Shopping Cart State and Go Shopping Button."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Empty State")
@allure.title("TC-057: Verify Empty Shopping Cart State and Go Shopping Button")
def test_issue_057_verify_empty_shopping_cart_state_and_go_shopping_button(
    catalog_page: CatalogPage,
) -> None:
    """Preconditions:
        No items have been added to the cart.

    Steps:
        1. Tap the shopping cart icon in the top header.

    Expected Result:
        The Cart screen opens showing "No Items" message and a "Go Shopping" button.
    """
    with allure.step("Precondition: No items have been added to the cart"):
        assert catalog_page.get_cart_item_count() == 0, (
            f"Expected initial cart count to be 0, got {catalog_page.get_cart_item_count()}"
        )

    with allure.step("Step 1: Tap the shopping cart icon in the top header"):
        catalog_page.navigate_to_cart()
        cart_page = CartPage(catalog_page.driver)

    with allure.step(
        "Expected Result: Cart screen opens showing 'No Items' message and a 'Go Shopping' button"
    ):
        assert cart_page.is_loaded(), "Cart screen did not load"
        assert cart_page.is_empty(), "Cart screen is not in empty state"
        assert cart_page.is_displayed(cart_page.NO_ITEMS_TITLE), (
            "'No Items' message is not displayed on empty cart screen"
        )
        assert cart_page.is_displayed(cart_page.GO_SHOPPING_BUTTON), (
            "'Go Shopping' button is not displayed on empty cart screen"
        )
