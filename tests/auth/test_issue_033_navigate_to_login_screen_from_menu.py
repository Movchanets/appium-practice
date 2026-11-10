"""Test scenario for navigating to login screen from drawer menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.auth
@pytest.mark.navigation
@allure.feature("Authentication")
@allure.story("Navigation to Login")
@allure.title("Navigate to Login Screen from Menu")
def test_issue_033_navigate_to_login_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        User is currently logged out.
    Steps:
        1. Open the navigation drawer menu.
        2. Tap "Log In".
    Expected Result:
        The Login screen opens displaying Username and Password fields, Login button,
        and quick autofill credentials.
    """
    with allure.step("Precondition: Ensure user is logged out"):
        catalog_page.logout_if_logged_in()

    with allure.step("Step 1: Open the navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.drawer_menu.is_open(), "Navigation drawer menu is not open"

    with allure.step("Step 2: Tap 'Log In'"):
        catalog_page.drawer_menu.click_login()

    with allure.step("Verify Login screen opens with required input fields and autofill"):
        login_page = LoginPage(catalog_page.driver)
        assert login_page.is_loaded(), "Login screen title is not displayed"
        assert login_page.is_displayed(login_page.USERNAME_INPUT), "Username field is not displayed"
        assert login_page.is_displayed(login_page.PASSWORD_INPUT), "Password field is not displayed"
        assert login_page.is_displayed(login_page.LOGIN_BUTTON), "Login button is not displayed"
        assert login_page.is_displayed(login_page.USER_BOD), "Autofill credentials not displayed"
