"""TC-041: Login Failure with Invalid Password."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Login Screen")
@allure.story("Login Validation")
@allure.title("TC-041: Login Failure with Invalid Password")
@allure.issue("41")
def test_issue_041_login_failure_with_invalid_password(login_page: LoginPage) -> None:
    """
    Preconditions:
        - User is on the Login screen.

    Steps:
        1. Enter "bod@example.com" in the Username field.
        2. Enter "incorrect_password" in the Password field.
        3. Tap the "Login" button.

    Expected Result:
        - An error message appears stating credentials do not match any user.
    """
    with allure.step("Precondition: Verify User is on Login screen"):
        assert login_page.is_loaded(), "Login screen is not displayed"

    with allure.step("Step 1: Enter 'bod@example.com' in the Username field"):
        login_page.enter_username("bod@example.com")

    with allure.step("Step 2: Enter 'incorrect_password' in the Password field"):
        login_page.enter_password("incorrect_password")

    with allure.step("Step 3: Tap the 'Login' button"):
        login_page.click_login_button()

    with allure.step("Verify error message appears stating credentials do not match any user"):
        assert login_page.is_error_displayed(), (
            "Error message was not displayed after submitting invalid password"
        )
        error_msg = login_page.get_error_message()
        assert len(error_msg) > 0, "Error message text is empty"
        assert (
            "do not match" in error_msg.lower()
            or "credentials" in error_msg.lower()
            or "sorry" in error_msg.lower()
        ), f"Unexpected error message text: '{error_msg}'"
