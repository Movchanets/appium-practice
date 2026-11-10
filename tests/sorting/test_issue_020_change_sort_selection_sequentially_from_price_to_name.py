"""Test scenario for changing sort selection sequentially from price to name."""

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
@allure.title("Change Sort Selection Sequentially from Price to Name")
@allure.issue("20")
def test_issue_020_change_sort_selection_sequentially_from_price_to_name(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap Sort and choose "Ascending order by price".
        2. Verify products sort by price low-to-high.
        3. Tap Sort again and choose "Ascending order by name".
        4. Verify products re-sort alphabetically A-to-Z.
    Expected Result:
        Catalog immediately re-sorts according to the newly selected criteria without lag or errors.
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap Sort and choose 'Ascending order by price'"):
        catalog_page.header.click_sort()
        catalog_page.sort_modal.sort_by_price_ascending()

    with allure.step("Step 2: Verify products sort by price low-to-high"):
        price_cards = catalog_page.get_product_cards()
        prices: list[float] = [
            float(card.get_price().replace("$", "").strip())
            for card in price_cards
            if card.get_price()
        ]
        assert len(prices) >= 2, "Expected at least 2 product prices"
        assert prices == sorted(prices), f"Products are not sorted by price ascending: {prices}"

    with allure.step("Step 3: Tap Sort again and choose 'Ascending order by name'"):
        catalog_page.header.click_sort()
        catalog_page.sort_modal.sort_by_name_ascending()

    with allure.step("Step 4: Verify products re-sort alphabetically A-to-Z"):
        name_cards = catalog_page.get_product_cards()
        titles = [card.get_title() for card in name_cards if card.get_title()]
        assert len(titles) >= 2, "Expected at least 2 product cards with titles"
        assert titles == sorted(titles), f"Products are not sorted alphabetically A to Z: {titles}"
