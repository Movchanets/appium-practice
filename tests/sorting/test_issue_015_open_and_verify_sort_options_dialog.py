"""Test scenario for opening and verifying sort options dialog."""

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.modals.sort_modal import SortModal


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.sorting
@allure.feature("Catalog Screen")
@allure.story("Sort Dialog")
@allure.title("Open and Verify Sort Options Dialog")
@allure.issue("15")
def test_issue_015_open_and_verify_sort_options_dialog(catalog_page: CatalogPage) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap the Sort button in the top navigation bar.
        2. Inspect the options displayed in the dialog.
    Expected Result:
        The sort dialog opens showing 4 options:
          - Name - Ascending
          - Name - Descending
          - Price - Ascending
          - Price - Descending
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap the Sort button in the top navigation bar"):
        catalog_page.header.click_sort()

    with allure.step("Step 2: Inspect the options displayed in the dialog"):
        sort_modal = catalog_page.sort_modal
        assert sort_modal.is_displayed(), "Sort modal dialog is not displayed"
        assert sort_modal.is_displayed(SortModal.NAME_ASC), (
            "'Ascending order by name' option is not displayed"
        )
        assert sort_modal.is_displayed(SortModal.NAME_DESC), (
            "'Descending order by name' option is not displayed"
        )
        assert sort_modal.is_displayed(SortModal.PRICE_ASC), (
            "'Ascending order by price' option is not displayed"
        )
        assert sort_modal.is_displayed(SortModal.PRICE_DESC), (
            "'Descending order by price' option is not displayed"
        )
