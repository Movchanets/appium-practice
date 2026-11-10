"""Test scenario for TC-051: Increase Item Quantity Using Plus Button."""

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
@allure.title("TC-051: Increase Item Quantity Using Plus Button")
@allure.issue("51")
def test_issue_051_increase_item_quantity_using_plus_button(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        User is on the Product Details screen with initial quantity 1.

    Steps:
        1. Tap the plus (+) button 3 times.

    Expected Result:
        The quantity counter increments to "4".
    """
    with allure.step("Precondition: User is on the Product Details screen with initial quantity 1"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"
        assert product_details_page.get_quantity() == 1, (
            f"Expected initial quantity 1, got {product_details_page.get_quantity()}"
        )

    with allure.step("Step 1: Tap the plus (+) button 3 times"):
        product_details_page.increase_quantity(times=3)

    with allure.step("Expected Result: The quantity counter increments to '4'"):
        actual_quantity = product_details_page.get_quantity()
        assert actual_quantity == 4, (
            f"Expected quantity counter to increment to 4, but got {actual_quantity}"
        )
