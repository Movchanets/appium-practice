"""Test scenario for sorting products by price in ascending order (Low to High)."""

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
@allure.title("Sort Products by Price in Ascending Order (Low to High)")
def test_issue_018_sort_products_by_price_in_ascending_order_low_to_high(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Tap the Sort button in the header.
        2. Select "Ascending order by price".
        3. Observe the product prices in the catalog.
    Expected Result:
        Products are arranged from least expensive to most expensive (e.g., $7.99, $9.99, $15.99).
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Tap the Sort button in the header"):
        catalog_page.header.click_sort()

    with allure.step("Step 2: Select 'Ascending order by price'"):
        catalog_page.sort_modal.sort_by_price_ascending()

    with allure.step("Step 3: Observe the product prices in the catalog"):
        cards = catalog_page.get_product_cards()
        prices: list[float] = [
            float(card.get_price().replace("$", "").strip()) for card in cards if card.get_price()
        ]
        assert len(prices) >= 2, "Expected at least 2 product prices"
        assert prices == sorted(prices), f"Products are not sorted by price ascending: {prices}"
