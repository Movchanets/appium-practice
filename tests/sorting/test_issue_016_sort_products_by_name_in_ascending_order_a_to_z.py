"""Test scenario for sorting products by name in ascending order (A to Z)."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.sorting
@allure.feature("Catalog Screen")
@allure.story("Product Sorting")
@allure.title("Sort Products by Name in Ascending Order (A to Z)")
def test_issue_016_sort_products_by_name_in_ascending_order_a_to_z(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap the Sort button in the header.
        2. Select "Ascending order by name".
        3. Observe the product titles in the catalog.
    Expected Result:
        The sort dialog closes.
        Products are arranged in alphabetical order A to Z
        (e.g., "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt").
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap the Sort button in the header"):
        catalog_page.header.click_sort()

    with allure.step("Step 2: Select 'Ascending order by name'"):
        catalog_page.sort_modal.sort_by_name_ascending()

    with allure.step("Step 3: Observe the product titles in the catalog"):
        cards = catalog_page.get_product_cards()
        titles = [card.get_title() for card in cards if card.get_title()]
        assert len(titles) >= 2, "Expected at least 2 product cards with titles"
        assert titles == sorted(titles), f"Products are not sorted alphabetically A to Z: {titles}"
        assert "Sauce Labs Backpack" in titles[0], (
            f"Expected 'Sauce Labs Backpack' to be first, got '{titles[0]}'"
        )
