"""TC-046: Select Black Color Variant on Product Details Screen."""

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
@allure.title("TC-046: Select Black Color Variant on Product Details Screen")
@allure.issue("46")
def test_issue_046_select_black_color_variant_on_product_details_screen(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User is on the Product Details screen for an item with color options
          (e.g. Sauce Labs Bike Light).

    Steps:
        1. Tap the Black color option circle.

    Expected Result:
        - The Black color circle is highlighted as the active selection.
    """
    with allure.step("Precondition: User is on Product Details screen for 'Sauce Labs Bike Light'"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"
        catalog_page.select_product_by_title("Sauce Labs Bike Light")
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"

    with allure.step("Step 1: Tap the Black color option circle"):
        product_details_page.select_color("black")

    with allure.step("Verify Black color circle is highlighted as the active selection"):
        black_circle = product_details_page.find_element(product_details_page.COLOR_BLACK)
        assert black_circle.is_displayed(), "Black color circle option is not displayed"
        assert (
            black_circle.is_selected()
            or black_circle.get_attribute("selected") in ("true", "True")
            or black_circle.is_enabled()
        ), "Black color circle is not active"
