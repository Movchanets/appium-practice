"""Test TC-096: Application Backgrounding and State Restoration Resilience."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.gestures_lifecycle
@allure.feature("Gestures & Lifecycle")
@allure.story("Application Backgrounding")
@allure.title("TC-096: Application Backgrounding and State Restoration Resilience")
@allure.issue("96")
def test_issue_096_application_backgrounding_and_state_restoration_resilience(
    catalog_page: CatalogPage,
) -> None:
    """Preconditions:
        App is running on the Catalog screen.
    Steps:
        1. Send the application to the background (simulate phone call or home button).
        2. Wait 3 seconds.
        3. Bring the application back to the foreground.
    Expected Result:
        App resumes seamlessly without crashing, and the Catalog screen remains active
        in its previous state.
    """
    with allure.step("Precondition: App is running on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"

    with allure.step("Steps 1-3: Send app to background for 3 seconds and bring back"):
        catalog_page.background_app(seconds=3)

    with allure.step("Verify app resumes seamlessly and Catalog screen remains active"):
        assert catalog_page.is_loaded(), (
            "Catalog screen is not loaded after resuming from background"
        )
        assert len(catalog_page.get_product_cards()) > 0, (
            "Product cards are missing after resuming from background"
        )
