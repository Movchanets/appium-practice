"""Test scenario for Issue 026: Navigate to WebView Screen from Menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.webview_page import WebViewPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Navigate to WebView Screen from Menu")
@allure.issue("26")
def test_issue_026_navigate_to_webview_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Navigation drawer menu is open.
    Steps:
        1. Tap "WebView" in the navigation menu.
    Expected Result:
        The drawer closes and the WebView screen opens displaying a URL input field
        and "Go" button.
    """
    with allure.step("Precondition: Open navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Navigation drawer menu is not open"
        )

    with allure.step("Step 1: Tap 'WebView' in the navigation menu"):
        catalog_page.drawer_menu.click_webview()

    with allure.step("Verify: WebView screen opens displaying URL input and 'Go' button"):
        webview_page = WebViewPage(catalog_page.driver)
        assert webview_page.is_loaded(), "WebView screen is not loaded"
        assert webview_page.is_displayed(webview_page.URL_INPUT), (
            "URL input field is not displayed on WebView screen"
        )
        assert webview_page.is_displayed(webview_page.GO_BUTTON), (
            "'Go' button is not displayed on WebView screen"
        )
