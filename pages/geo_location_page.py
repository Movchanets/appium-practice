"""Geo Location Page Object."""

from __future__ import annotations

import sys
import time

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class GeoLocationPage(BasePage):
    """Page Object encapsulating Geo Location tracking screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/locationTV")
    LATITUDE_TEXT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/latitudeTV")
    LONGITUDE_TEXT: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/longitudeTV",
    )
    START_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/startBtn")
    STOP_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/stopBtn")

    def is_loaded(self) -> bool:
        """Check if Geo Location title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def set_mock_location(
        self,
        latitude: float = 37.7749,
        longitude: float = -122.4194,
        altitude: float = 0.0,
    ) -> Self:
        """Set mock GPS coordinates on device/emulator (gracefully ignored if unsupported)."""
        try:
            self.driver.set_location(latitude, longitude, altitude)
        except Exception:
            pass
        return self

    def start_location(self) -> Self:
        """Tap 'Start Observing' button."""
        self.click(self.START_BUTTON)
        return self

    def stop_location(self) -> Self:
        """Tap 'Stop Observing' button."""
        self.click(self.STOP_BUTTON)
        return self

    def get_latitude(self) -> str:
        """Retrieve displayed latitude value."""
        return self.get_text(self.LATITUDE_TEXT)

    def get_longitude(self) -> str:
        """Retrieve displayed longitude value."""
        return self.get_text(self.LONGITUDE_TEXT)

    def wait_for_valid_coordinates(self, timeout: float = 10.0) -> tuple[str, str]:
        """Poll until latitude and longitude contain valid non-null numeric digits."""
        end_time = time.time() + timeout
        lat = self.get_latitude()
        lon = self.get_longitude()
        while time.time() < end_time:
            lat = self.get_latitude()
            lon = self.get_longitude()
            if (
                lat
                and lon
                and lat.lower() != "null"
                and lon.lower() != "null"
                and any(c.isdigit() for c in lat)
                and any(c.isdigit() for c in lon)
            ):
                return lat, lon
            time.sleep(0.5)
        return lat, lon

    def grant_location_permission(self, allow: bool = True) -> Self:
        """Handle system location permission alert."""
        self.handle_permission_alert(allow=allow)
        return self

    def is_latitude_displayed(self, timeout: float = 3.0) -> bool:
        """Check if latitude display field is visible."""
        return self.is_displayed(self.LATITUDE_TEXT, timeout=timeout)

    def is_longitude_displayed(self, timeout: float = 3.0) -> bool:
        """Check if longitude display field is visible."""
        return self.is_displayed(self.LONGITUDE_TEXT, timeout=timeout)

    def is_start_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Start Observing button is visible."""
        return self.is_displayed(self.START_BUTTON, timeout=timeout)

    def is_stop_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Stop Observing button is visible."""
        return self.is_displayed(self.STOP_BUTTON, timeout=timeout)
