"""Test scenario for Issue 030: Navigate to About Screen from Menu."""

from __future__ import annotations

import allure
import pytest

from pages.about_page import AboutPage
from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Navigate to About Screen from Menu")
@allure.issue("30")
def test_issue_030_navigate_to_about_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Navigation drawer menu is open.
    Steps:
        1. Tap "About" in the navigation menu.
    Expected Result:
        The About screen opens displaying app version information and the Sauce Labs
        website link.
    """
    with allure.step("Precondition: Open navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Navigation drawer menu is not open"
        )

    with allure.step("Step 1: Tap 'About' in the navigation menu"):
        catalog_page.drawer_menu.click_about()

    with allure.step("Verify: About screen opens displaying version info and website link"):
        about_page = AboutPage(catalog_page.driver)
        assert about_page.is_loaded(), "About screen is not loaded"
        assert about_page.is_displayed(about_page.VERSION_TEXT), (
            "App version text is not displayed on About screen"
        )
        assert len(about_page.get_version().strip()) > 0, "App version string is empty"
        assert about_page.is_displayed(about_page.WEB_LINK), (
            "Sauce Labs website link is not displayed on About screen"
        )
