"""Test scenario for Issue 025: Open and View Navigation Drawer Menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Open and View Navigation Drawer Menu")
@allure.issue("25")
def test_issue_025_open_and_view_navigation_drawer_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is on the Catalog screen.
    Steps:
        1. Tap the hamburger menu button in the top-left corner.
    Expected Result:
        The slide navigation drawer menu opens from the left, displaying all
        available navigation options.
    """
    with allure.step("Step 1: Tap the hamburger menu button in the top-left corner"):
        catalog_page.header.click_menu()

    with allure.step("Verify: Navigation drawer menu opens displaying available options"):
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Slide navigation drawer menu is not displayed"
        )
        drawer = catalog_page.drawer_menu
        assert drawer.is_displayed(drawer.MENU_CATALOG_ITEM), (
            "Catalog menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_WEBVIEW_ITEM), (
            "WebView menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_QR_CODE_ITEM), (
            "QR Code Scanner menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_GEO_LOCATION_ITEM), (
            "Geo Location menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_DRAWING_ITEM), (
            "Drawing menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_ABOUT_ITEM), (
            "About menu item is not displayed in drawer"
        )
        assert drawer.is_displayed(drawer.MENU_RESET_APP_ITEM), (
            "Reset App State menu item is not displayed in drawer"
        )
