"""Login Page Object for Sauce Labs Demo App."""

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object encapsulating elements and actions for the Authentication Screen."""

    # Locators prioritized: ACCESSIBILITY_ID > relative XPATH
    USERNAME_INPUT = (
        AppiumBy.XPATH,
        "//*[@content-desc='Username input field'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/nameET']",
    )
    PASSWORD_INPUT = (
        AppiumBy.XPATH,
        "//*[@content-desc='Password input field'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/passwordET']",
    )
    LOGIN_BUTTON = (
        AppiumBy.XPATH,
        "//*[@content-desc='Login button'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/loginBtn']",
    )
    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[@resource-id='com.saucelabs.mydemoapp.android:id/passwordErrorTV'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/nameErrorTV'] "
        "| //*[contains(@resource-id, 'Error') or contains(@resource-id, 'error') "
        "or contains(@text, 'match') or contains(@text, 'Sorry') or contains(@text, 'locked out')]",
    )
    BIOMETRICS_SWITCH = (AppiumBy.ACCESSIBILITY_ID, "biometrics-switch")

    def enter_username(self, username: str) -> Self:
        """Fill the username input field."""
        self.send_keys(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> Self:
        """Fill the password input field."""
        self.send_keys(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> Self:
        """Tap the login submission button."""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> Self:
        """Fluent helper executing complete credential entry and submission."""
        self.enter_username(username)
        self.enter_password(password)
        self.hide_keyboard()
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """Retrieve the authentication error text displayed on failure."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self, timeout: float = 7.0) -> bool:
        """Check whether the authentication error banner is visible."""
        return self.is_displayed(self.ERROR_MESSAGE, timeout=timeout)
