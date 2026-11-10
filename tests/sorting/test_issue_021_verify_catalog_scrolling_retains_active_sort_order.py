"""Test scenario for Issue 021: Verify Catalog Scrolling Retains Active Sort Order."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.sorting
@allure.feature("Catalog Screen")
@allure.story("Sorting")
@allure.title("Verify Catalog Scrolling Retains Active Sort Order")
@allure.issue("21")
def test_issue_021_verify_catalog_scrolling_retains_active_sort_order(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Products are sorted by Name Descending (Z to A).
    Steps:
        1. Scroll down the catalog to view lower items.
        2. Observe product order.
    Expected Result:
        The descending alphabetical sort order is preserved throughout the entire catalog
        as user scrolls.
    """
    with allure.step("Precondition: Products are sorted by Name Descending (Z to A)"):
        catalog_page.sort_products("name_desc")
        initial_cards = catalog_page.get_product_cards()
        initial_titles = [card.get_title() for card in initial_cards]
        assert len(initial_titles) > 0, "No product cards displayed after sorting"
        assert initial_titles == sorted(initial_titles, reverse=True), (
            f"Initial products not sorted descending: {initial_titles}"
        )

    with allure.step("Step 1: Scroll down the catalog to view lower items"):
        catalog_page.scroll_catalog_down()

    with allure.step("Step 2: Observe product order"):
        scrolled_cards = catalog_page.get_product_cards()
        scrolled_titles = [card.get_title() for card in scrolled_cards]
        assert len(scrolled_titles) > 0, "No product cards displayed after scrolling down"
        assert scrolled_titles == sorted(scrolled_titles, reverse=True), (
            f"Visible items after scroll not sorted descending: {scrolled_titles}"
        )

    with allure.step("Verify: Descending alphabetical sort order is preserved across catalog"):
        combined_titles: list[str] = []
        for title in initial_titles + scrolled_titles:
            if title not in combined_titles:
                combined_titles.append(title)
        assert combined_titles == sorted(combined_titles, reverse=True), (
            f"Overall catalog product sequence is not in descending order: {combined_titles}"
        )
