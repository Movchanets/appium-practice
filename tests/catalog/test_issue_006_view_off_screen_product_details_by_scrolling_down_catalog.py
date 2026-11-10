"""TC-006: View Off-Screen Product Details by Scrolling Down Catalog."""

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
@allure.story("Catalog Scrolling")
@allure.title("TC-006: View Off-Screen Product Details by Scrolling Down Catalog")
@allure.issue("6")
def test_issue_006_view_off_screen_product_details_by_scrolling_down_catalog(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen; target product "Sauce Labs Onesie" is initially
          below the fold.

    Steps:
        1. Scroll down the catalog until reaching the "Sauce Labs Onesie".
        2. Tap on the "Sauce Labs Onesie" product card.

    Expected Result:
        - The catalog scrolls smoothly without lag or visual glitches.
        - Tapping the item opens the Product Details screen for "Sauce Labs Onesie".
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Scroll down the catalog until reaching the 'Sauce Labs Onesie'"):
        catalog_page.scroll_to_text("Sauce Labs Onesie")
        card = catalog_page.get_product_card_by_title("Sauce Labs Onesie")
        assert card.is_visible(), "'Sauce Labs Onesie' card is not visible after scrolling"

    with allure.step("Step 2: Tap on the 'Sauce Labs Onesie' product card"):
        card.click_item()

    with allure.step("Verify Product Details screen opens for 'Sauce Labs Onesie'"):
        assert product_details_page.is_loaded(), "Product Details screen failed to load"
        assert product_details_page.get_title() == "Sauce Labs Onesie"
