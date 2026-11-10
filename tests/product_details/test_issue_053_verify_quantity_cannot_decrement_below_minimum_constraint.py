"""Test scenario for TC-053: Verify Quantity Cannot Decrement Below Minimum Constraint."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Quantity Management")
@allure.title("TC-053: Verify Quantity Cannot Decrement Below Minimum Constraint")
def test_issue_053_verify_quantity_cannot_decrement_below_minimum_constraint(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        User is on the Product Details screen with quantity 1.

    Steps:
        1. Tap the minus (-) button.

    Expected Result:
        The quantity remains at 1 (or becomes 0 with Add to Cart button disabled);
        it never goes negative.
    """
    with allure.step("Precondition: User is on the Product Details screen with quantity 1"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"
        assert product_details_page.get_quantity() == 1, (
            f"Expected initial quantity 1, got {product_details_page.get_quantity()}"
        )

    with allure.step("Step 1: Tap the minus (-) button"):
        product_details_page.decrease_quantity(times=1)

    with allure.step(
        "Expected Result: The quantity remains at 1 (or >= 0) and never goes negative"
    ):
        actual_quantity = product_details_page.get_quantity()
        assert actual_quantity >= 1, (
            f"Quantity decremented below minimum constraint of 1, current value: {actual_quantity}"
        )
