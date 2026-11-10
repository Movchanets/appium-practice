"""Test scenario for sorting products by name in descending order (Z to A)."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.sorting
@allure.feature("Catalog Screen")
@allure.story("Product Sorting")
@allure.title("Sort Products by Name in Descending Order (Z to A)")
def test_issue_017_sort_products_by_name_in_descending_order_z_to_a(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap the Sort button in the header.
        2. Select "Descending order by name".
        3. Observe the product titles in the catalog.
    Expected Result:
        Products are arranged in reverse alphabetical order Z to A
        (e.g., "Test.allTheThings() T-Shirt" appears first).
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap the Sort button in the header"):
        catalog_page.header.click_sort()

    with allure.step("Step 2: Select 'Descending order by name'"):
        catalog_page.sort_modal.sort_by_name_descending()

    with allure.step("Step 3: Observe the product titles in the catalog"):
        cards = catalog_page.get_product_cards()
        titles = [card.get_title() for card in cards if card.get_title()]
        assert len(titles) >= 2, "Expected at least 2 product cards with titles"
        assert titles == sorted(titles, reverse=True), (
            f"Products are not sorted reverse alphabetically Z to A: {titles}"
        )
        assert "Test.allTheThings()" in titles[0], (
            f"Expected 'Test.allTheThings()' product to be first, got '{titles[0]}'"
        )
