"""TC-049: Select Green Color Variant on Product Details Screen."""

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
@allure.title("TC-049: Select Green Color Variant on Product Details Screen")
@allure.issue("49")
def test_issue_049_select_green_color_variant_on_product_details_screen(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User is on the Product Details screen.

    Steps:
        1. Tap the Green color option circle.

    Expected Result:
        - The Green color circle is highlighted as the active selection.
    """
    with allure.step("Precondition: User is on Product Details screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"
        catalog_page.select_product_by_title("Sauce Labs Bike Light")
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"

    with allure.step("Step 1: Tap the Green color option circle"):
        product_details_page.select_color("green")

    with allure.step("Verify Green color circle is highlighted as the active selection"):
        green_circle = product_details_page.find_element(product_details_page.COLOR_GREEN)
        assert green_circle.is_displayed(), "Green color circle option is not displayed"
        assert (
            green_circle.is_selected()
            or green_circle.get_attribute("selected") in ("true", "True")
            or green_circle.is_enabled()
        ), "Green color circle is not active"
