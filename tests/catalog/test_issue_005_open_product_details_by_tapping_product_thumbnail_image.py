"""TC-005: Open Product Details by Tapping Product Thumbnail Image."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@allure.feature("Product Catalog")
@allure.story("Product Navigation")
@allure.title("TC-005: Open Product Details by Tapping Product Thumbnail Image")
def test_issue_005_open_product_details_by_tapping_product_thumbnail_image(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen.

    Steps:
        1. Locate the item "Sauce Labs Backpack".
        2. Tap directly on the product thumbnail image.

    Expected Result:
        - The Product Details screen opens displaying the selected product.
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Locate the item 'Sauce Labs Backpack'"):
        card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        assert card.is_visible(), "Sauce Labs Backpack card is not visible"

    with allure.step("Step 2: Tap directly on the product thumbnail image"):
        card.click_image()

    with allure.step("Verify Product Details screen opens displaying the selected product"):
        assert product_details_page.is_loaded(), "Product Details screen failed to load"
        assert product_details_page.get_title() == "Sauce Labs Backpack"
