"""TC-001: Verify Product Catalog Screen Loads on App Launch."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
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
        assert catalog_page.is_loaded(), "Catalog page failed to load on app launch"

    with allure.step("Step 1: Observe the top header"):
        assert catalog_page.header.is_title_displayed(), "Header title / logo is not displayed"

    with allure.step("Step 2: Observe the product catalog grid content"):
        cards = catalog_page.get_product_cards()
        assert len(cards) >= 2, "Expected at least 2 product cards in catalog grid"
        for i in range(2):
            card = cards[i]
            assert card.get_title(), f"Product card {i} title is empty"
            assert card.get_price(), f"Product card {i} price is empty"
            assert card.is_image_displayed(), f"Product card {i} image is not displayed"
