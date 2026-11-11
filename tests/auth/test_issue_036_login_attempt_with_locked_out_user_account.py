"""Test scenario for login attempt with locked-out user account."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Login Validation")
@allure.title("Login Attempt with Locked-Out User Account")
@allure.issue("36")
def test_issue_036_login_attempt_with_locked_out_user_account(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Tap on the sample credentials for locked-out user "alice@example.com"
           (or enter alice@example.com / 10203040).
        2. Tap the "Login" button.
    Expected Result:
        Login fails and an error message is displayed: "Sorry, this user has been locked out.".
    """
    with allure.step("Step 1: Tap on sample credentials for locked-out user 'alice@example.com'"):
        login_page.autofill_alice()
        assert "alice@example.com" in login_page.get_username(), (
            "Username was not autofilled for locked-out user"
        )

    with allure.step("Step 2: Tap the 'Login' button"):
        login_page.click_login_button()

    with allure.step("Verify login fails and locked-out error message is displayed"):
        assert login_page.is_error_displayed(), "Locked-out error message is not displayed"
        error_message = login_page.get_error_message()
        assert "Sorry, this user has been locked out." in error_message, (
            f"Expected locked-out error message, but got: '{error_message}'"
        )
