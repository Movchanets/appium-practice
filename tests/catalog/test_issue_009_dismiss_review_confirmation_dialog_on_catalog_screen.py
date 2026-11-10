"""TC-009: Dismiss Review Confirmation Dialog on Catalog Screen."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@allure.feature("Product Catalog")
@allure.story("Review Modal Dialog")
@allure.title("TC-009: Dismiss Review Confirmation Dialog on Catalog Screen")
@allure.issue("9")
def test_issue_009_dismiss_review_confirmation_dialog_on_catalog_screen(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - A review confirmation dialog is displayed after submitting a star rating.

    Steps:
        1. Tap the "Close" button on the review popup dialog.

    Expected Result:
        - The popup dialog closes and the user returns to the interactive catalog without
          screen freezing.
    """
    with allure.step("Precondition: Submit a star rating to display review confirmation dialog"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page is not loaded"
        card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        card.click_rating_star(5)
        review_modal = catalog_page.review_modal
        assert review_modal.is_displayed(), "Review modal is not displayed in precondition"

    with allure.step("Step 1: Tap the 'Close' button on the review popup dialog"):
        review_modal.close()

    with allure.step("Verify popup dialog closes and user returns to interactive catalog"):
        assert not review_modal.is_displayed(), (
            "Review modal is still displayed after clicking Close"
        )
        assert catalog_page.is_loaded(), (
            "Catalog screen is not active or interactive after dismissing modal"
        )
