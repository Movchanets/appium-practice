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
@allure.issue("53")
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
        if actual_quantity == 0:
            assert (
                not product_details_page.is_add_to_cart_displayed(timeout=1.0)
                or not product_details_page.find_element(
                    product_details_page.ADD_TO_CART_BUTTON
                ).is_enabled()
            )
        else:
            assert actual_quantity == 1, f"Expected quantity to remain at 1, got {actual_quantity}"
