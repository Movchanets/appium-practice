"""TC-043: Cancel Logout from Confirmation Dialog."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage
from pages.modals.confirmation_modal import ConfirmationModal


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.auth
@allure.feature("Login Screen")
@allure.story("Logout Flow")
@allure.title("TC-043: Cancel Logout from Confirmation Dialog")
@allure.issue("43")
def test_issue_043_cancel_logout_from_confirmation_dialog(
    login_page: LoginPage,
    confirmation_modal: ConfirmationModal,
) -> None:
    """
    Preconditions:
        - User is logged in and the logout confirmation dialog is displayed.

    Steps:
        1. Tap "Cancel" on the logout confirmation popup.

    Expected Result:
        - The popup closes and the user remains logged in.
    """
    with allure.step("Precondition: User is logged in and logout confirmation dialog is displayed"):
        assert login_page.is_loaded(), "Login screen is not displayed"
        login_page.login("bod@example.com", "10203040")
        assert login_page.is_logged_in(), "User failed to log in for precondition"
        login_page.open_menu()
        login_page.drawer_menu.click_logout()
        assert confirmation_modal.is_displayed(), "Logout confirmation dialog is not displayed"

    with allure.step("Step 1: Tap 'Cancel' on the logout confirmation popup"):
        confirmation_modal.dismiss()

    with allure.step("Verify popup closes and user remains logged in"):
        assert not confirmation_modal.is_displayed(timeout=2.0), (
            "Logout confirmation dialog did not close after dismissal"
        )
        login_page.open_menu()
        assert login_page.drawer_menu.is_logged_in(), (
            "User should remain logged in after canceling logout"
        )
