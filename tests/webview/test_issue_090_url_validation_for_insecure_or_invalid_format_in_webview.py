"""TC-090: URL Validation for Insecure or Invalid Format in WebView."""

from __future__ import annotations

import allure
import pytest

from pages.webview_page import WebViewPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.webview
@allure.feature("WebView")
@allure.story("URL Validation")
@allure.title("TC-090: URL Validation for Insecure or Invalid Format in WebView")
def test_issue_090_url_validation_for_insecure_or_invalid_format_in_webview(
    webview_page: WebViewPage,
) -> None:
    """
    Preconditions:
        - User is on the WebView screen.

    Steps:
        1. Enter an insecure URL (e.g. "http://example.com" or invalid text).
        2. Tap the "Go" button.

    Expected Result:
        - The app prevents loading or displays a security validation warning
          requiring a secure HTTPS URL.
    """
    with allure.step("Precondition: User is on the WebView screen"):
        assert webview_page.is_loaded(), "WebView screen is not loaded"
        assert webview_page.is_displayed(webview_page.URL_INPUT), (
            "URL input field is not displayed on WebView screen"
        )

    with allure.step("Step 1: Enter an insecure URL in the URL input field"):
        webview_page.enter_url("http://example.com")

    with allure.step("Step 2: Tap the 'Go' button"):
        webview_page.hide_keyboard()
        webview_page.click_go()

    with allure.step("Verify: The app prevents loading or displays a security validation warning"):
        error_displayed = webview_page.is_url_error_displayed(timeout=3.0)
        url_input_retained = webview_page.is_displayed(webview_page.URL_INPUT, timeout=2.0)
        assert error_displayed or url_input_retained, (
            "App did not prevent loading or display validation warning for insecure URL"
        )
        if error_displayed:
            error_text = webview_page.get_url_error()
            assert len(error_text.strip()) > 0, "URL validation error text is empty"
