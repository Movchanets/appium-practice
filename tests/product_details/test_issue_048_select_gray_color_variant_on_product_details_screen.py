"""TC-048: Select Gray Color Variant on Product Details Screen."""

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
@allure.story("Color Selection")
@allure.title("TC-048: Select Gray Color Variant on Product Details Screen")
@allure.issue("48")
def test_issue_048_select_gray_color_variant_on_product_details_screen(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User is on the Product Details screen.

    Steps:
        1. Tap the Gray color option circle.

    Expected Result:
        - The Gray color circle is highlighted as the active selection.
    """
    with allure.step("Precondition: User is on Product Details screen for 'Sauce Labs Backpack'"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"

    with allure.step("Step 1: Tap the Gray color option circle"):
        product_details_page.select_color("gray")

    with allure.step("Verify Gray color circle is highlighted as the active selection"):
        assert product_details_page.is_displayed(product_details_page.COLOR_GRAY), (
            "Gray color circle option is not displayed"
        )
        assert product_details_page.is_color_selected("gray"), "Gray color circle is not active"
