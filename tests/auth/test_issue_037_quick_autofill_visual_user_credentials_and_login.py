"""Test scenario for quick autofill visual user credentials and login."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Quick Autofill")
@allure.title("Quick Autofill Visual User Credentials and Login")
def test_issue_037_quick_autofill_visual_user_credentials_and_login(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Tap on the sample credentials text for visual user "visual@example.com".
        2. Tap the "Login" button.
    Expected Result:
        Credentials autofill and login succeeds, redirecting to the Catalog screen.
    """
    with allure.step("Step 1: Tap on sample credentials for visual user 'visual@example.com'"):
        login_page.autofill_visual()
        assert login_page.get_username() == "visual@example.com", (
            "Username was not autofilled for visual user"
        )

    with allure.step("Step 2: Tap the 'Login' button"):
        login_page.click_login_button()

    with allure.step("Verify login succeeds and user is authenticated"):
        assert login_page.is_logged_in(), (
            "User was not successfully authenticated with visual user credentials"
        )
