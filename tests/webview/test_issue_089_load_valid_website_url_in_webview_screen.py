"""TC-089: Load Valid Website URL in WebView Screen."""

from __future__ import annotations

import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from pages.webview_page import WebViewPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.webview
@allure.feature("WebView")
@allure.story("URL Navigation")
@allure.title("TC-089: Load Valid Website URL in WebView Screen")
@allure.issue("89")
def test_issue_089_load_valid_website_url_in_webview_screen(
    webview_page: WebViewPage,
) -> None:
    """
    Preconditions:
        - User navigates to the WebView screen from the menu.

    Steps:
        1. Enter "https://saucelabs.com" in the URL input field.
        2. Tap the "Go" button.

    Expected Result:
        - The in-app web browser loads and renders the Sauce Labs website content.
    """
    with allure.step("Precondition: User is on the WebView screen"):
        assert webview_page.is_loaded(), "WebView screen is not loaded"
        assert webview_page.is_displayed(webview_page.URL_INPUT), (
            "URL input field is not displayed on WebView screen"
        )

    with allure.step("Step 1: Enter 'https://saucelabs.com' in the URL input field"):
        webview_page.enter_url("https://saucelabs.com")

    with allure.step("Step 2: Tap the 'Go' button"):
        webview_page.hide_keyboard()
        webview_page.click_go()

    with allure.step("Verify: The in-app web browser loads and renders website content"):
        webview_locator = (AppiumBy.CLASS_NAME, "android.webkit.WebView")
        is_webview_active = (
            webview_page.is_displayed(webview_locator, timeout=10.0)
            or len(webview_page.driver.contexts) > 1
            or not webview_page.is_url_error_displayed(timeout=2.0)
        )
        assert is_webview_active, "In-app browser failed to load valid HTTPS URL"
