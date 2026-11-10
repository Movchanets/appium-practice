"""TC-002: Verify Product Card Information in Catalog."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Product Catalog")
@allure.story("Product Card Details")
@allure.title("TC-002: Verify Product Card Information in Catalog")
@allure.issue("2")
def test_issue_002_verify_product_card_information_in_catalog(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen.

    Steps:
        1. Inspect the first product card displayed in the grid ("Sauce Labs Backpack").
        2. Check the product image, title, price, and star ratings.

    Expected Result:
        - Product title displays as "Sauce Labs Backpack".
        - Product price displays as "$ 29.99".
        - Thumbnail image is clearly visible, and 5 interactive rating stars are displayed.
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Inspect the 'Sauce Labs Backpack' product card in the grid"):
        card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        assert card.is_visible(), "Sauce Labs Backpack card is not visible"

    with allure.step("Step 2: Check the product image, title, price, and star ratings"):
        assert card.get_title() == "Sauce Labs Backpack", "Product title does not match expected"
        assert card.get_price() == "$ 29.99", "Product price does not match expected"
        assert card.is_displayed(card.IMAGE), "Thumbnail image is not displayed"
        assert card.is_displayed(card.STAR_1), "Star 1 is not displayed"
        assert card.is_displayed(card.STAR_2), "Star 2 is not displayed"
        assert card.is_displayed(card.STAR_3), "Star 3 is not displayed"
        assert card.is_displayed(card.STAR_4), "Star 4 is not displayed"
        assert card.is_displayed(card.STAR_5), "Star 5 is not displayed"
