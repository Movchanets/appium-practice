"""TC-010: Submit 3-Star Rating and Dismiss Confirmation Dialog."""

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
@allure.title("TC-010: Submit 3-Star Rating and Dismiss Confirmation Dialog")
@allure.issue("10")
def test_issue_010_submit_3_star_rating_and_dismiss_confirmation_dialog(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen.

    Steps:
        1. On the "Sauce Labs Bolt T-Shirt" card, tap the 3rd star icon.
        2. Verify the thank-you message is displayed in the popup.
        3. Tap the "Close" button.

    Expected Result:
        - The confirmation popup opens displaying the thank-you message and dismisses
          cleanly upon tapping Close.
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: On the 'Sauce Labs Bolt T-Shirt' card, tap the 3rd star icon"):
        catalog_page.scroll_to_text("Sauce Labs Bolt T-Shirt")
        card = catalog_page.get_product_card_by_title("Sauce Labs Bolt T-Shirt")
        card.click_rating_star(3)

    with allure.step("Step 2: Verify the thank-you message is displayed in the popup"):
        review_modal = catalog_page.review_modal
        assert review_modal.is_displayed(), "Review confirmation modal is not displayed"
        assert review_modal.get_message() == "Thank you for submitting your review!", (
            "Review confirmation message text does not match expected"
        )

    with allure.step("Step 3: Tap the 'Close' button"):
        review_modal.close()

    with allure.step("Verify confirmation popup dismisses cleanly"):
        assert not review_modal.is_displayed(), (
            "Review modal is still displayed after clicking Close"
        )
        assert catalog_page.is_loaded(), (
            "Catalog screen is not active or interactive after dismissing modal"
        )
