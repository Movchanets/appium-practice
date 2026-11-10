"""Test scenario for form validation when submitting empty username."""

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
@allure.title("Form Validation when Submitting Empty Username")
@allure.issue("40")
def test_issue_040_form_validation_when_submitting_empty_username(
    login_page: LoginPage,
) -> None:
    """
    Preconditions:
        User is on the Login screen.
    Steps:
        1. Leave the Username field blank.
        2. Enter "10203040" in the Password field.
        3. Tap the "Login" button.
    Expected Result:
        Form submission is blocked and a validation error message appears: "Username is required".
    """
    with allure.step("Step 1 & 2: Leave Username blank and enter '10203040' in Password field"):
        login_page.enter_password("10203040")

    with allure.step("Step 3: Tap the 'Login' button"):
        login_page.hide_keyboard()
        login_page.click_login_button()

    with allure.step("Verify form submission is blocked with 'Username is required'"):
        assert login_page.is_error_displayed(), "Username validation error is not displayed"
        error_message = login_page.get_username_error()
        assert "Username is required" in error_message, (
            f"Expected 'Username is required', but got: '{error_message}'"
        )
