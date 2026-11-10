"""Test TC-092: Start Real-Time Location Tracking in Geo Location Screen."""

from __future__ import annotations

import allure
import pytest

from pages.geo_location_page import GeoLocationPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.device_features
@allure.feature("Device Features")
@allure.story("Geo Location")
@allure.title("TC-092: Start Real-Time Location Tracking in Geo Location Screen")
def test_issue_092_start_real_time_location_tracking_in_geo_location_screen(
    geo_location_page: GeoLocationPage,
) -> None:
    """Preconditions:
        User navigates to Geo Location screen and grants location permission.
    Steps:
        1. Tap the 'Start Observing' button.
        2. Observe the Latitude and Longitude values.
    Expected Result:
        Real-time coordinates update displaying numeric latitude and longitude values.
    """
    with allure.step("Precondition: Handle permission alert and ensure screen loaded"):
        geo_location_page.handle_permission_alert(allow=True)
        assert geo_location_page.is_loaded(), "Geo Location screen is not loaded"

    with allure.step("Step 1: Tap the 'Start Observing' button"):
        geo_location_page.start_location()

    with allure.step("Step 2: Observe Latitude and Longitude values"):
        latitude = geo_location_page.get_latitude()
        longitude = geo_location_page.get_longitude()
        assert latitude != "", "Latitude text is empty"
        assert longitude != "", "Longitude text is empty"
        assert any(char.isdigit() for char in latitude), (
            f"Latitude '{latitude}' does not contain numeric digits"
        )
        assert any(char.isdigit() for char in longitude), (
            f"Longitude '{longitude}' does not contain numeric digits"
        )
