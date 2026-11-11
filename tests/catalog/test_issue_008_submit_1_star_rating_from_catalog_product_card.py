"""TC-008: Submit 1-Star Rating from Catalog Product Card."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Product Catalog")
@allure.story("Product Rating")
@allure.title("TC-008: Submit 1-Star Rating from Catalog Product Card")
@allure.issue("8")
def test_issue_008_submit_1_star_rating_from_catalog_product_card(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen.

    Steps:
        1. On the "Sauce Labs Bike Light" card, tap the 1st star icon.

    Expected Result:
        - A review confirmation popup appears with the message:
          "Thank you for submitting your review!".
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: On the 'Sauce Labs Bike Light' card, tap the 1st star icon"):
        catalog_page.scroll_to_text("Sauce Labs Bike Light")
        card = catalog_page.get_product_card_by_title("Sauce Labs Bike Light")
        card.click_rating_star(1)

    with allure.step("Verify review confirmation popup appears with thank-you message"):
        review_modal = catalog_page.review_modal
        assert review_modal.is_displayed(), "Review confirmation modal is not displayed"
        assert review_modal.get_message() == "Thank you for submitting your review!", (
            "Review confirmation message text does not match expected"
        )
        review_modal.close()
