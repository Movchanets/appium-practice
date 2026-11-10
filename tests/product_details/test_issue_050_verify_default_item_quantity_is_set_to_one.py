"""TC-050: Verify Default Item Quantity is Set to One."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Quantity Management")
@allure.title("TC-050: Verify Default Item Quantity is Set to One")
@allure.issue("50")
def test_issue_050_verify_default_item_quantity_is_set_to_one(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User opens any product on the Product Details screen.

    Steps:
        1. Check the quantity counter between the minus and plus buttons.

    Expected Result:
        - The quantity displays "1".
    """
    with allure.step("Precondition: User opens a product on the Product Details screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"

    with allure.step("Step 1 & Verification: Check counter between minus and plus buttons"):
        quantity = product_details_page.get_quantity()
        raw_quantity_text = product_details_page.get_text(
            product_details_page.QUANTITY_TEXT
        ).strip()
        assert quantity == 1, f"Expected default quantity to be 1, but got {quantity}"
        assert raw_quantity_text == "1", (
            f"Expected quantity display text '1', but got '{raw_quantity_text}'"
        )
