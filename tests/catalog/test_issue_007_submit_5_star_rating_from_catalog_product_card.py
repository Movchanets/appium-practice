"""TC-007: Submit 5-Star Rating from Catalog Product Card."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@allure.feature("Product Catalog")
@allure.story("Product Rating")
@allure.title("TC-007: Submit 5-Star Rating from Catalog Product Card")
@allure.issue("7")
def test_issue_007_submit_5_star_rating_from_catalog_product_card(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen with products visible.

    Steps:
        1. On the "Sauce Labs Backpack" card, tap the 5th star icon.
        2. Observe the dialog that appears.

    Expected Result:
        - A review confirmation popup appears with the message:
          "Thank you for submitting your review!".
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: On the 'Sauce Labs Backpack' card, tap the 5th star icon"):
        card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        card.click_rating_star(5)

    with allure.step("Step 2: Observe the dialog that appears"):
        review_modal = catalog_page.review_modal
        assert review_modal.is_displayed(), "Review confirmation modal is not displayed"
        assert review_modal.get_message() == "Thank you for submitting your review!", (
            "Review confirmation message text does not match expected"
        )
        review_modal.close()
