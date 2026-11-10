"""Test scenario for Issue 028: Navigate to Geo Location Screen from Menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.geo_location_page import GeoLocationPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Navigate to Geo Location Screen from Menu")
@allure.issue("28")
def test_issue_028_navigate_to_geo_location_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Navigation drawer menu is open.
    Steps:
        1. Tap "Geo Location" in the navigation menu.
    Expected Result:
        The Geo Location screen opens displaying GPS coordinates and observing controls.
    """
    with allure.step("Precondition: Open navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Navigation drawer menu is not open"
        )

    with allure.step("Step 1: Tap 'Geo Location' in the navigation menu"):
        catalog_page.drawer_menu.click_geo_location()

    with allure.step("Verify: Geo Location screen opens with GPS coordinates and controls"):
        geo_page = GeoLocationPage(catalog_page.driver)
        geo_page.handle_permission_alert(allow=True)
        assert geo_page.is_loaded(), "Geo Location screen is not loaded"
        assert geo_page.is_displayed(geo_page.START_BUTTON), (
            "'Start Observing' button is not displayed on Geo Location screen"
        )
        assert geo_page.is_displayed(geo_page.LATITUDE_TEXT), (
            "Latitude coordinate display is not visible on Geo Location screen"
        )
        assert geo_page.is_displayed(geo_page.LONGITUDE_TEXT), (
            "Longitude coordinate display is not visible on Geo Location screen"
        )
