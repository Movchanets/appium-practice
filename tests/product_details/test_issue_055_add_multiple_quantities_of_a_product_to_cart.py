"""Test scenario for TC-055: Add Multiple Quantities of a Product to Cart."""

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
@allure.story("Add To Cart")
@allure.title("TC-055: Add Multiple Quantities of a Product to Cart")
@allure.issue("55")
def test_issue_055_add_multiple_quantities_of_a_product_to_cart(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        User is on the Product Details screen.

    Steps:
        1. Increase item quantity to 3 using the plus button.
        2. Tap the "Add to Cart" button.

    Expected Result:
        The items are added and the shopping cart badge count updates to "3".
    """
    with allure.step("Precondition: User is on the Product Details screen"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"

    with allure.step("Step 1: Increase item quantity to 3 using the plus button"):
        product_details_page.increase_quantity(times=2)
        assert product_details_page.get_quantity() == 3, (
            f"Expected quantity to be 3, but got {product_details_page.get_quantity()}"
        )

    with allure.step("Step 2: Tap the 'Add to Cart' button"):
        product_details_page.add_to_cart()

    with allure.step(
        "Expected Result: The items are added and shopping cart badge count updates to '3'"
    ):
        badge_count = product_details_page.header.get_cart_item_count()
        assert badge_count == 3, f"Expected cart badge count to update to 3, but got {badge_count}"
