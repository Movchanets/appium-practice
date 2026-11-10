"""Test scenario for Issue 029: Navigate to Drawing Screen from Menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.drawing_page import DrawingPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Navigate to Drawing Screen from Menu")
@allure.issue("29")
def test_issue_029_navigate_to_drawing_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Navigation drawer menu is open.
    Steps:
        1. Tap "Drawing" in the navigation menu.
    Expected Result:
        The Drawing screen opens with a drawing pad, "Clear", and "Save" buttons.
    """
    with allure.step("Precondition: Open navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Navigation drawer menu is not open"
        )

    with allure.step("Step 1: Tap 'Drawing' in the navigation menu"):
        catalog_page.drawer_menu.click_drawing()

    with allure.step("Verify: Drawing screen opens with drawing pad, 'Clear', and 'Save' buttons"):
        drawing_page = DrawingPage(catalog_page.driver)
        assert drawing_page.is_loaded(), "Drawing screen is not loaded"
        assert drawing_page.is_displayed(drawing_page.SIGNATURE_PAD), (
            "Drawing signature pad is not displayed"
        )
        assert drawing_page.is_displayed(drawing_page.CLEAR_BUTTON), (
            "'Clear' button is not displayed on Drawing screen"
        )
        assert drawing_page.is_displayed(drawing_page.SAVE_BUTTON), (
            "'Save' button is not displayed on Drawing screen"
        )
