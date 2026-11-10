"""TC-001: Verify Product Catalog Screen Loads on App Launch."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@allure.feature("Product Catalog")
@allure.story("Catalog Screen Launch")
@allure.title("TC-001: Verify Product Catalog Screen Loads on App Launch")
@allure.issue("1")
def test_issue_001_verify_product_catalog_screen_loads_on_app_launch(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        - Sauce Labs Demo App is installed on the Android device.
        - App is launched from a clean state.

    Steps:
        1. Open the application.
        2. Observe the main screen header and content area.

    Expected Result:
        - The top header displays the Sauce Labs logo and app title.
        - The product catalog grid loads cleanly, displaying available items with titles,
          prices, and images.
    """
    with allure.step("Precondition: App is opened on the Catalog screen"):
        if not catalog_page.is_displayed(catalog_page.PRODUCT_ITEMS, timeout=2.0):
            catalog_page.open_menu()
            catalog_page.drawer_menu.click_catalog()
        assert catalog_page.is_loaded(), "Catalog page failed to load on app launch"

    with allure.step("Step 1: Observe the top header"):
        assert catalog_page.header.is_title_displayed(), "Header title / logo is not displayed"

    with allure.step("Step 2: Observe the product catalog grid content"):
        cards = catalog_page.get_product_cards()
        assert len(cards) > 0, "No product cards found in catalog grid"
        first_card = cards[0]
        assert first_card.get_title(), "First product card title is empty"
        assert first_card.get_price(), "First product card price is empty"
        assert first_card.is_displayed(first_card.IMAGE), (
            "First product thumbnail image is not displayed"
        )
