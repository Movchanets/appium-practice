"""Test scenario for sorting products by price in descending order (High to Low)."""

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
@allure.title("Sort Products by Price in Descending Order (High to Low)")
@allure.issue("19")
def test_issue_019_sort_products_by_price_in_descending_order_high_to_low(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap the Sort button in the header.
        2. Select "Descending order by price".
        3. Observe the product prices in the catalog.
    Expected Result:
        Products are arranged from most expensive to least expensive
        (e.g., $49.99 Fleece Jacket appears first).
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap the Sort button in the header"):
        catalog_page.header.click_sort()

    with allure.step("Step 2: Select 'Descending order by price'"):
        catalog_page.sort_modal.sort_by_price_descending()

    with allure.step("Step 3: Observe the product prices in the catalog"):
        cards = catalog_page.get_product_cards()
        prices: list[float] = [
            float(card.get_price().replace("$", "").strip()) for card in cards if card.get_price()
        ]
        assert len(prices) >= 2, "Expected at least 2 product prices"
        assert prices == sorted(prices, reverse=True), (
            f"Products are not sorted by price descending: {prices}"
        )
        assert prices[0] >= 49.0, f"Expected most expensive item (>= $49) first, got ${prices[0]}"
