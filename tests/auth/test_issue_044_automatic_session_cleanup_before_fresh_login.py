"""TC-044: Automatic Session Cleanup Before Fresh Login."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage
from pages.modals.confirmation_modal import ConfirmationModal


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Login Screen")
@allure.story("Session Management")
@allure.title("TC-044: Automatic Session Cleanup Before Fresh Login")
@allure.issue("44")
def test_issue_044_automatic_session_cleanup_before_fresh_login(
    catalog_page: CatalogPage,
    confirmation_modal: ConfirmationModal,
) -> None:
    """
    Preconditions:
        - App may have a lingering session from a previous test run.

    Steps:
        1. Open navigation menu.
        2. If logged in, perform logout and confirm.
        3. Navigate to Login screen.

    Expected Result:
        - The user starts cleanly from the unauthenticated Login screen without session collisions.
    """
    with allure.step("Precondition: Ensure an active session is present"):
        catalog_page.open_menu()
        if not catalog_page.drawer_menu.is_logged_in():
            catalog_page.drawer_menu.click_login()
            login_p = LoginPage(catalog_page.driver)
            login_p.login("bod@example.com", "10203040")
            catalog_page.open_menu()
        assert catalog_page.drawer_menu.is_logged_in(), (
            "Precondition failed: active session is not present"
        )

    with allure.step("Step 1: Open navigation menu"):
        catalog_page.open_menu()
        assert catalog_page.drawer_menu.is_open(), "Navigation drawer menu is not open"

    with allure.step("Step 2: If logged in, perform logout and confirm"):
        if catalog_page.drawer_menu.is_logged_in():
            catalog_page.drawer_menu.click_logout()
            assert confirmation_modal.is_displayed(), "Logout confirmation modal is not displayed"
            confirmation_modal.confirm()

    with allure.step("Step 3: Navigate to Login screen"):
        catalog_page.open_menu()
        assert not catalog_page.drawer_menu.is_logged_in(), (
            "Session was not terminated prior to navigation"
        )
        catalog_page.drawer_menu.click_login()

    with allure.step("Verify user starts cleanly from unauthenticated Login screen"):
        login_page = LoginPage(catalog_page.driver)
        assert login_page.is_loaded(), "Login screen did not load"
        assert login_page.get_username() == "", "Username field is not clean and empty"
        assert not login_page.is_error_displayed(timeout=1.0), (
            "Lingering error message displayed on fresh Login screen"
        )
