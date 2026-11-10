"""Test scenario for TC-052: Decrease Item Quantity Using Minus Button."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Quantity Management")
@allure.title("TC-052: Decrease Item Quantity Using Minus Button")
@allure.issue("52")
def test_issue_052_decrease_item_quantity_using_minus_button(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        User is on the Product Details screen with quantity set to 3.

    Steps:
        1. Tap the minus (-) button once.

    Expected Result:
        The quantity counter decrements from "3" to "2".
    """
    with allure.step("Precondition: User is on the Product Details screen with quantity set to 3"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"
        product_details_page.increase_quantity(times=2)
        assert product_details_page.get_quantity() == 3, (
            f"Expected initial quantity 3, got {product_details_page.get_quantity()}"
        )

    with allure.step("Step 1: Tap the minus (-) button once"):
        product_details_page.decrease_quantity(times=1)

    with allure.step("Expected Result: The quantity counter decrements from '3' to '2'"):
        actual_quantity = product_details_page.get_quantity()
        assert actual_quantity == 2, (
            f"Expected quantity counter to decrement to 2, but got {actual_quantity}"
        )
