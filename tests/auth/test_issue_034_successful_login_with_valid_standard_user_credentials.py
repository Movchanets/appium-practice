"""Test scenario stub."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password",
    [
        ("bod@example.com", "10203040"),
        ("visual@example.com", "10203040"),
    ],
)
def test_issue_034_successful_login_with_valid_standard_user_credentials(
    login_page: LoginPage, username: str, password: str
) -> None:
    """
    Steps
    1.Enter username in username field
    2.Enter password in password field
    3.Click on login button

    :param login_page:
    :param username:
    :param password:
    :return:
    """
    with allure.step(f"Enter {username}"):
        login_page.enter_username(username)

    with allure.step(f"Enter {password}"):
        login_page.enter_password(password)

    with allure.step("Click on login button"):
        login_page.click_login_button()
    with allure.step("Verify successful login"):
        assert login_page.is_logged_in()
