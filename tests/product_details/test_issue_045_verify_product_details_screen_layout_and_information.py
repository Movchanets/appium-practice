"""TC-045: Verify Product Details Screen Layout and Information."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Product Layout")
@allure.title("TC-045: Verify Product Details Screen Layout and Information")
@allure.issue("45")
def test_issue_045_verify_product_details_screen_layout_and_information(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - User is on the Catalog screen.

    Steps:
        1. Tap on "Sauce Labs Backpack".
        2. Observe the product details screen.

    Expected Result:
        - The screen displays product title ("Sauce Labs Backpack"), price ("$ 29.99"),
          full description, product image, color selectors, and quantity controls.
    """
    with allure.step("Precondition: User is on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"

    with allure.step("Step 1: Tap on 'Sauce Labs Backpack'"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")

    with allure.step("Step 2 & Verification: Observe the product details screen"):
        assert product_details_page.is_loaded(), "Product Details screen is not loaded"
        assert product_details_page.get_title() == "Sauce Labs Backpack", (
            f"Expected title 'Sauce Labs Backpack', got '{product_details_page.get_title()}'"
        )
        assert product_details_page.get_price() == "$ 29.99", (
            f"Expected price '$ 29.99', got '{product_details_page.get_price()}'"
        )
        assert product_details_page.is_displayed(product_details_page.PRODUCT_IMAGE), (
            "Product image is not displayed"
        )
        assert product_details_page.is_displayed(product_details_page.COLOR_BLACK), (
            "Color selectors are not displayed"
        )
        assert product_details_page.is_displayed(product_details_page.MINUS_BUTTON), (
            "Quantity minus button is not displayed"
        )
        assert product_details_page.is_displayed(product_details_page.PLUS_BUTTON), (
            "Quantity plus button is not displayed"
        )
        assert product_details_page.is_displayed(product_details_page.QUANTITY_TEXT), (
            "Quantity counter text is not displayed"
        )
        assert len(product_details_page.get_description()) > 0, "Product description is empty"
