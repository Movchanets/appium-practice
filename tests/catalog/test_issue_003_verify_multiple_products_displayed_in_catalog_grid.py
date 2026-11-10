"""TC-003: Verify Multiple Products Displayed in Catalog Grid."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Product Catalog")
@allure.story("Catalog Grid Display")
@allure.title("TC-003: Verify Multiple Products Displayed in Catalog Grid")
@allure.issue("3")
def test_issue_003_verify_multiple_products_displayed_in_catalog_grid(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen in portrait mode.

    Steps:
        1. Observe the products displayed in the catalog view.

    Expected Result:
        - Multiple product cards are arranged in a clean two-column grid with clear spacing
          and readable details.
    """
    with allure.step("Precondition: Verify device orientation is Portrait and Catalog is loaded"):
        if catalog_page.get_orientation() != "PORTRAIT":
            catalog_page.rotate_to_portrait()
        assert catalog_page.get_orientation() == "PORTRAIT", "Screen orientation is not Portrait"

    with allure.step("Step 1: Observe the products displayed in the catalog view"):
        cards = catalog_page.get_product_cards()
        assert len(cards) >= 2, f"Expected at least 2 product cards, found {len(cards)}"

    with allure.step("Verify cards are arranged in a multi-column grid with readable details"):
        loc_card1 = cards[0].root.location
        loc_card2 = cards[1].root.location
        assert loc_card1["x"] != loc_card2["x"], (
            "First two product cards do not form a multi-column grid"
        )

        visible_cards = [card for card in cards if card.get_title()]
        assert len(visible_cards) >= 2, (
            f"Expected multiple visible product cards, found {len(visible_cards)}"
        )

        for idx, card in enumerate(visible_cards, start=1):
            assert card.is_visible(), f"Product card #{idx} is not visible"
            assert card.get_price() != "", f"Product card #{idx} has an empty price"
