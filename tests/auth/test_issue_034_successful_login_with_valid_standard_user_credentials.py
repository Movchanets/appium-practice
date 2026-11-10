"""Test scenario for successful login with valid credentials."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Login")
@allure.title("Successful Login with Valid Standard User Credentials")
@allure.issue("34")
def test_issue_034_successful_login_with_valid_standard_user_credentials(
    login_page: LoginPage,
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
    with allure.step("Step 1: Enter standard username 'bod@example.com'"):
        login_page.enter_username("bod@example.com")

    with allure.step("Step 2: Enter password '10203040'"):
        login_page.enter_password("10203040")

    with allure.step("Step 3: Click on login button"):
        login_page.hide_keyboard()
        login_page.click_login_button()

    with allure.step(
        "Verify successful login, redirection to Catalog screen, and drawer displays 'Log Out'"
    ):
        catalog_page = CatalogPage(login_page.driver)
        assert catalog_page.is_loaded(), "User was not redirected to Catalog screen after login"
        assert login_page.is_logged_in(), "User is not logged in after providing valid credentials"
