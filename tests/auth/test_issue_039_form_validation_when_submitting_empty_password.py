"""Test scenario for form validation when submitting empty password."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Form Validation")
@allure.title("Form Validation when Submitting Empty Password")
def test_issue_039_form_validation_when_submitting_empty_password(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Enter "bod@example.com" in the Username field.
        2. Leave the Password field blank.
        3. Tap the "Login" button.
    Expected Result:
        Form submission is blocked and a validation error message appears: "Enter Password".
    """
    with allure.step("Step 1: Enter 'bod@example.com' in the Username field"):
        login_page.enter_username("bod@example.com")

    with allure.step("Step 2 & 3: Leave Password field blank and tap 'Login' button"):
        login_page.hide_keyboard()
        login_page.click_login_button()

    with allure.step("Verify form submission is blocked with 'Enter Password'"):
        assert login_page.is_error_displayed(), "Password validation error is not displayed"
        error_message = login_page.get_password_error()
        assert "Enter Password" in error_message, (
            f"Expected 'Enter Password', but got: '{error_message}'"
        )
