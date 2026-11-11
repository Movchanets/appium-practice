"""Test scenario for verifying independent information display across product cards."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Catalog Screen")
@allure.story("Product Grid")
@allure.title("Verify Independent Information Display Across Product Cards")
@allure.issue("12")
def test_issue_012_verify_independent_information_display_across_product_cards(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen with multiple items visible.
    Steps:
        1. Compare the first two visible product cards
           (e.g. "Sauce Labs Backpack" and "Sauce Labs Bike Light").
    Expected Result:
        Each product card displays its own unique title, price, and thumbnail image
        without overlapping or incorrect data.
    """
    with allure.step("Precondition: App is open on the Catalog screen with multiple items visible"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"
        cards = catalog_page.get_product_cards()
        assert len(cards) >= 2, "Expected at least 2 product cards visible in the catalog"

    with allure.step("Step 1: Compare the first two visible product cards"):
        card1, card2 = cards[0], cards[1]
        title1 = card1.get_title()
        title2 = card2.get_title()
        price1 = card1.get_price()
        price2 = card2.get_price()

        assert title1, "First product card title is empty"
        assert title2, "Second product card title is empty"
        assert title1 != title2, f"Product cards share identical title: '{title1}'"

        assert price1, "First product card price is empty"
        assert price2, "Second product card price is empty"
        assert price1.startswith("$"), f"First product card price format invalid: '{price1}'"
        assert price2.startswith("$"), f"Second product card price format invalid: '{price2}'"

        assert card1.is_image_displayed(), "First product thumbnail is not displayed"
        assert card2.is_image_displayed(), "Second product thumbnail is not displayed"
