"""Drawing Screen Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from pages.base_page import BasePage
from pages.types import Locator


class DrawingPage(BasePage):
    """Page Object encapsulating Drawing signature pad screen."""

    TITLE: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/drawingTV")
    SIGNATURE_PAD: Locator = (
        AppiumBy.ID,
        "com.saucelabs.mydemoapp.android:id/signature_pad",
    )
    CLEAR_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/clearBtn")
    SAVE_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/saveBtn")

    def is_loaded(self) -> bool:
        """Check if Drawing screen title is visible."""
        return self.is_displayed(self.TITLE, timeout=5.0)

    def draw_signature(self) -> Self:
        """Execute a stroke gesture across the signature pad."""
        pad = self.find_element(self.SIGNATURE_PAD)
        loc = pad.location
        size = pad.size

        start_x = loc["x"] + int(size["width"] * 0.2)
        start_y = loc["y"] + int(size["height"] * 0.5)
        end_x = loc["x"] + int(size["width"] * 0.8)
        end_y = loc["y"] + int(size["height"] * 0.5)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.2)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        return self

    def clear(self) -> Self:
        """Tap 'Clear' button to erase pad."""
        self.click(self.CLEAR_BUTTON)
        return self

    def save(self) -> Self:
        """Tap 'Save' button to save signature."""
        self.click(self.SAVE_BUTTON)
        return self

    def is_signature_pad_displayed(self, timeout: float = 3.0) -> bool:
        """Check if signature pad canvas is visible."""
        return self.is_displayed(self.SIGNATURE_PAD, timeout=timeout)

    def is_clear_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Clear button is visible."""
        return self.is_displayed(self.CLEAR_BUTTON, timeout=timeout)

    def is_save_button_displayed(self, timeout: float = 3.0) -> bool:
        """Check if Save button is visible."""
        return self.is_displayed(self.SAVE_BUTTON, timeout=timeout)
