"""Test scenario for form validation when submitting empty username and password."""

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
@allure.title("Form Validation when Submitting Empty Username and Password")
@allure.issue("38")
def test_issue_038_form_validation_when_submitting_empty_username_and_password(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen with empty fields.
    Steps:
        1. Leave both Username and Password fields empty.
        2. Tap the "Login" button.
    Expected Result:
        Form submission is blocked and a validation error message appears: "Username is required".
    """
    with allure.step("Precondition: User is on the Login screen with empty fields"):
        assert login_page.is_loaded(), "Login screen is not loaded"

    with allure.step("Step 1 & 2: Leave both fields empty and tap the 'Login' button"):
        login_page.click_login_button()

    with allure.step("Verify form submission is blocked with 'Username is required'"):
        assert login_page.is_error_displayed(), "Validation error message is not displayed"
        error_message = login_page.get_username_error()
        assert "Username is required" in error_message, (
            f"Expected 'Username is required', but got: '{error_message}'"
        )
