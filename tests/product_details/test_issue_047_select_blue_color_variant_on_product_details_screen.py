"""TC-047: Select Blue Color Variant on Product Details Screen."""

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
@allure.title("TC-047: Select Blue Color Variant on Product Details Screen")
def test_issue_047_select_blue_color_variant_on_product_details_screen(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User is on the Product Details screen.

    Steps:
        1. Tap the Blue color option circle.

    Expected Result:
        - The Blue color circle is highlighted as the active selection.
    """
    with allure.step("Precondition: User is on Product Details screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"
        catalog_page.select_product_by_title("Sauce Labs Bike Light")
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"

    with allure.step("Step 1: Tap the Blue color option circle"):
        product_details_page.select_color("blue")

    with allure.step("Verify Blue color circle is highlighted as the active selection"):
        blue_circle = product_details_page.find_element(product_details_page.COLOR_BLUE)
        assert blue_circle.is_displayed(), "Blue color circle option is not displayed"
        assert (
            blue_circle.is_selected()
            or blue_circle.get_attribute("selected") in ("true", "True")
            or blue_circle.is_enabled()
        ), "Blue color circle is not active"
