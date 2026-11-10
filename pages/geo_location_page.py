"""Geo Location Page Object."""

from __future__ import annotations

import sys

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
