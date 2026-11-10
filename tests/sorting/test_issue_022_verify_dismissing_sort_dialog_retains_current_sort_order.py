"""Test scenario for Issue 022: Verify Dismissing Sort Dialog Retains Current Sort Order."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.sorting
@allure.feature("Catalog Screen")
@allure.story("Sorting")
@allure.title("Verify Dismissing Sort Dialog Retains Current Sort Order")
def test_issue_022_verify_dismissing_sort_dialog_retains_current_sort_order(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Catalog has a specific sort order active.
    Steps:
        1. Tap the Sort button to open the sort dialog.
        2. Tap outside the dialog or press the device Back button to dismiss it without
           selecting an option.
    Expected Result:
        The sort dialog closes and the existing product sort order remains unchanged.
    """
    with allure.step("Precondition: Catalog has a specific sort order active"):
        catalog_page.sort_products("name_asc")
        initial_cards = catalog_page.get_product_cards()
        initial_titles = [card.get_title() for card in initial_cards]
        assert len(initial_titles) > 0, "No product cards displayed in catalog"

    with allure.step("Step 1: Tap the Sort button to open the sort dialog"):
        catalog_page.header.click_sort()
        assert catalog_page.sort_modal.is_displayed(), "Sort modal dialog is not displayed"

    with allure.step("Step 2: Dismiss sort dialog without selecting an option"):
        catalog_page.sort_modal.dismiss()
        assert not catalog_page.sort_modal.is_displayed(timeout=2.0), (
            "Sort modal is still displayed after dismissal"
        )

    with allure.step("Verify: Existing product sort order remains unchanged"):
        current_cards = catalog_page.get_product_cards()
        current_titles = [card.get_title() for card in current_cards]
        assert current_titles == initial_titles, (
            f"Product sort order changed after dismissing sort dialog. "
            f"Expected {initial_titles}, got {current_titles}"
        )
