"""Test scenario for successful login with valid credentials."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Login")
@allure.title("Successful Login with Valid Standard User Credentials")
@pytest.mark.parametrize(
    "username, password",
    [
        ("bod@example.com", "10203040"),
        ("visual@example.com", "10203040"),
    ],
)
@allure.issue("34")
def test_issue_034_successful_login_with_valid_standard_user_credentials(
    login_page: LoginPage, username: str, password: str
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Enter username in the Username field.
        2. Enter password in the Password field.
        3. Tap the "Login" button.
    Expected Result:
        User is successfully authenticated and redirected to the Catalog screen.
        Navigation drawer now displays "Log Out" instead of "Log In".
    """
    with allure.step(f"Step 1: Enter '{username}' in username field"):
        login_page.enter_username(username)

    with allure.step("Step 2: Enter password in password field"):
        login_page.enter_password(password)

    with allure.step("Step 3: Click on login button"):
        login_page.hide_keyboard()
        login_page.click_login_button()

    with allure.step("Verify successful login and drawer displays 'Log Out'"):
        assert login_page.is_logged_in(), "User is not logged in after providing valid credentials"
