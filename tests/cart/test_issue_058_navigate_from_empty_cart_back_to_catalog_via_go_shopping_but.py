"""Test scenario for TC-058: Navigate from Empty Cart Back to Catalog via Go Shopping Button."""

from __future__ import annotations

import allure
import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.cart
@allure.feature("Cart")
@allure.story("Empty State Navigation")
@allure.title("TC-058: Navigate from Empty Cart Back to Catalog via Go Shopping Button")
@allure.issue("58")
def test_issue_058_navigate_from_empty_cart_back_to_catalog_via_go_shopping_but(
    cart_page: CartPage,
) -> None:
    """Preconditions:
        User is on the empty Cart screen.

    Steps:
        1. Tap the "Go Shopping" button.

    Expected Result:
        User is navigated back to the Catalog screen displaying products.
    """
    with allure.step("Precondition: User is on the empty Cart screen"):
        assert cart_page.is_loaded(), "Cart screen did not load"
        assert cart_page.is_empty(), "Cart screen is not empty"
        assert cart_page.is_displayed(cart_page.GO_SHOPPING_BUTTON), (
            "'Go Shopping' button is not displayed"
        )

    with allure.step("Step 1: Tap the 'Go Shopping' button"):
        cart_page.click_go_shopping()

    with allure.step(
        "Expected Result: User is navigated back to the Catalog screen displaying products"
    ):
        catalog_page = CatalogPage(cart_page.driver)
        assert catalog_page.is_loaded(), "User was not navigated back to the Catalog screen"
        product_cards = catalog_page.get_product_cards()
        assert len(product_cards) > 0, "Catalog screen displays no products"
