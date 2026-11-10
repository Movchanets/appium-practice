"""TC-042: Successful Logout via Navigation Drawer."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage
from pages.modals.confirmation_modal import ConfirmationModal


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Login Screen")
@allure.story("Logout Flow")
@allure.title("TC-042: Successful Logout via Navigation Drawer")
def test_issue_042_successful_logout_via_navigation_drawer(
    login_page: LoginPage,
    confirmation_modal: ConfirmationModal,
) -> None:
    """
    Preconditions:
        - User is logged in with an active session.

    Steps:
        1. Open the navigation drawer menu.
        2. Tap "Log Out".
        3. On the logout confirmation dialog, tap "Log Out".

    Expected Result:
        - The session is terminated and the navigation drawer menu now displays "Log In".
    """
    with allure.step("Precondition: User is logged in with an active session"):
        assert login_page.is_loaded(), "Login screen is not displayed"
        login_page.login("bod@example.com", "10203040")
        assert login_page.is_logged_in(), "User failed to log in for precondition"

    with allure.step("Step 1: Open the navigation drawer menu"):
        login_page.open_menu()
        assert login_page.drawer_menu.is_open(), "Navigation drawer menu is not open"

    with allure.step("Step 2: Tap 'Log Out'"):
        login_page.drawer_menu.click_logout()
        assert confirmation_modal.is_displayed(), "Logout confirmation dialog is not displayed"

    with allure.step("Step 3: On the logout confirmation dialog, tap 'Log Out'"):
        confirmation_modal.confirm()

    with allure.step("Verify session is terminated and navigation drawer displays 'Log In'"):
        login_page.open_menu()
        assert not login_page.drawer_menu.is_logged_in(), (
            "User session was not terminated after logout"
        )
        assert login_page.drawer_menu.is_displayed(login_page.drawer_menu.MENU_LOGIN_ITEM), (
            "Navigation drawer menu does not display 'Log In'"
        )
