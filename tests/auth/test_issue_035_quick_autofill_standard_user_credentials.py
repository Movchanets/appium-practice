"""Test scenario for quick autofill standard user credentials."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Quick Autofill")
@allure.title("Quick Autofill Standard User Credentials")
@allure.issue("35")
def test_issue_035_quick_autofill_standard_user_credentials(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Tap on the sample credentials text for standard user "bod@example.com".
        2. Tap the "Login" button.
    Expected Result:
        Username and password fields autofill with standard user credentials.
        Login succeeds and navigates to the Catalog screen.
    """
    with allure.step("Step 1: Tap sample credentials for standard user 'bod@example.com'"):
        login_page.autofill_bod()
        assert login_page.get_username() == "bod@example.com", (
            "Username field was not autofilled with standard user credentials"
        )
        assert len(login_page.get_password()) > 0, "Password field was not autofilled"

    with allure.step("Step 2: Tap the 'Login' button"):
        login_page.click_login_button()

    with allure.step("Verify login succeeds and user is authenticated on Catalog screen"):
        catalog_page = CatalogPage(login_page.driver)
        assert catalog_page.is_loaded(), "User was not redirected to Catalog screen"
        assert login_page.is_logged_in(), (
            "User was not successfully authenticated with autofill credentials"
        )
