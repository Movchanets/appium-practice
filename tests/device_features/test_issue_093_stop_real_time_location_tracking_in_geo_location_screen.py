"""Test TC-093: Stop Real-Time Location Tracking in Geo Location Screen."""

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
@allure.title("TC-093: Stop Real-Time Location Tracking in Geo Location Screen")
def test_issue_093_stop_real_time_location_tracking_in_geo_location_screen(
    geo_location_page: GeoLocationPage,
) -> None:
    """Preconditions:
        Location tracking is actively observing.
    Steps:
        1. Tap the 'Stop Observing' button.
    Expected Result:
        Location tracking stops updating cleanly without app lag or crashes.
    """
    with allure.step("Precondition: Start observing location tracking"):
        geo_location_page.handle_permission_alert(allow=True)
        assert geo_location_page.is_loaded(), "Geo Location screen is not loaded"
        geo_location_page.start_location()

    with allure.step("Step 1: Tap the 'Stop Observing' button"):
        geo_location_page.stop_location()

    with allure.step("Verify tracking stopped and screen remains active without crashes"):
        assert geo_location_page.is_loaded(), (
            "Geo Location screen is no longer loaded after stopping observing"
        )
