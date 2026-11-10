"""Test TC-095: Verify Application Version and External Link on About Screen."""

from __future__ import annotations

import allure
import pytest

from pages.about_page import AboutPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.device_features
@allure.feature("Device Features")
@allure.story("About")
@allure.title("TC-095: Verify Application Version and External Link on About Screen")
@allure.issue("95")
def test_issue_095_verify_application_version_and_external_link_on_about_screen(
    about_page: AboutPage,
) -> None:
    """Preconditions:
        User navigates to the About screen from the menu.
    Steps:
        1. Inspect the app version text.
        2. Check the Sauce Labs website link.
    Expected Result:
        App version is displayed (e.g. 'V.1.3.0') and the website link is visible and clickable.
    """
    with allure.step("Precondition: User navigates to About screen"):
        assert about_page.is_loaded(), "About screen is not loaded"

    with allure.step("Step 1: Inspect the app version text"):
        version = about_page.get_version()
        assert version != "", "App version string is empty"
        assert "V." in version or any(char.isdigit() for char in version), (
            f"Unexpected app version format: '{version}'"
        )

    with allure.step("Step 2: Check Sauce Labs website link is visible"):
        assert about_page.is_displayed(about_page.WEB_LINK), (
            "Sauce Labs website link is not displayed"
        )
        about_page.click_web_link()
