"""Reference production-grade smoke tests for Mobile ATQC candidates.

Demonstrates:
- Clean Page Object Model composition.
- Dynamic gesture execution (relative window percentage swipe).
- Device state handling (app backgrounding & foreground resilience).
- Explicit synchronization without arbitrary sleeps.
"""

import pytest
from appium.webdriver.webdriver import WebDriver

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.mobile
@pytest.mark.smoke
class TestMobileSmokeSuite:
    """Production reference test suite for core mobile workflows."""

    def test_catalog_display_and_navigation(self, driver: WebDriver) -> None:
        """Verify catalog items are rendered and menu interaction works."""
        catalog_page = CatalogPage(driver)

        # Assert catalog screen header is visible
        assert catalog_page.is_loaded(), "Expected Catalog screen to be loaded"

        # Interacting with slide menu
        catalog_page.open_menu()

    def test_dynamic_catalog_swipe(self, driver: WebDriver) -> None:
        """Verify dynamic vertical swiping on catalog grid using relative screen dimensions."""
        catalog_page = CatalogPage(driver)
        assert catalog_page.is_loaded(), "Catalog should be loaded before swiping"

        # Execute dynamic gesture calculated from window bounds (no hardcoded pixels)
        catalog_page.swipe_up(duration_ms=700)

        # Verify page remains stable and responsive after gesture
        assert catalog_page.is_loaded(), "Catalog must remain functional after swipe gesture"

    def test_app_background_resilience(self, driver: WebDriver) -> None:
        """Verify application lifecycle handling when placed in the background.

        In mobile environments, apps are regularly interrupted by incoming calls,
        notifications, and user multitasking. The app must resume gracefully
        without crashes or losing session state.
        """
        catalog_page = CatalogPage(driver)
        assert catalog_page.is_loaded(), "Initial screen should be active"

        # Put app into background for 3 seconds, Appium automatically brings it back
        catalog_page.background_app(seconds=3)

        # Assert UI state restored intact
        assert catalog_page.is_loaded(), "Application should resume in active state without crash"

    def test_invalid_login_validation_flow(self, driver: WebDriver) -> None:
        """Verify authentication error display with proper explicit wait assertions."""
        catalog_page = CatalogPage(driver)
        catalog_page.navigate_to_login()

        login_page = LoginPage(driver)
        # Attempt login with locked-out user in the Android demo app
        login_page.login(username="alice@example.com", password="10203040")

        # Verify user feedback
        assert login_page.is_error_displayed(), "Validation error banner must appear"
        error_msg = login_page.get_error_message()
        assert len(error_msg) > 0, "Error message text must not be empty"
        assert "locked out" in error_msg.lower() or "sorry" in error_msg.lower()
