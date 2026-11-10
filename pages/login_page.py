"""Login Page Object for Sauce Labs Demo App."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.types import Locator


class LoginPage(BasePage):
    """Page Object encapsulating elements and actions for the Authentication Screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginTV")
    USERNAME_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
    PASSWORD_INPUT: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET")
    LOGIN_BUTTON: Locator = (
        AppiumBy.ACCESSIBILITY_ID,
        "Tap to login with given credentials",
    )
    USERNAME_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
    PASSWORD_ERROR: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordErrorTV")
    ERROR_MESSAGE: Locator = (
        AppiumBy.XPATH,
        '//*[@resource-id="com.saucelabs.mydemoapp.android:id/passwordErrorTV" '
        'or @resource-id="com.saucelabs.mydemoapp.android:id/nameErrorTV"]',
    )
    USER_BOD: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV")
    USER_ALICE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username2TV")
    USER_VISUAL: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username3TV")

    def is_loaded(self) -> bool:
        """Check if login screen title is displayed."""
        return self.is_displayed(self.TITLE, timeout=5.0)

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

    def autofill_bod(self) -> Self:
        """Tap sample credentials for standard user bod@example.com."""
        self.click(self.USER_BOD)
        return self

    def autofill_alice(self) -> Self:
        """Tap sample credentials for locked out user alice@example.com."""
        self.click(self.USER_ALICE)
        return self

    def autofill_visual(self) -> Self:
        """Tap sample credentials for visual user visual@example.com."""
        self.click(self.USER_VISUAL)
        return self

    def get_username_error(self) -> str:
        """Retrieve username validation error text."""
        return self.get_text(self.USERNAME_ERROR)

    def get_password_error(self) -> str:
        """Retrieve password validation error text."""
        return self.get_text(self.PASSWORD_ERROR)

    def get_error_message(self) -> str:
        """Retrieve any authentication error text displayed on failure."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self, timeout: float = 5.0) -> bool:
        """Check whether any authentication error is visible."""
        return self.is_displayed(self.ERROR_MESSAGE, timeout=timeout)
