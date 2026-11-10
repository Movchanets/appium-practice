"""Test scenario for Issue 023: Verify Top Navigation Header Layout and Branding."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Top Navigation Header")
@allure.title("Verify Top Navigation Header Layout and Branding")
@allure.issue("23")
def test_issue_023_verify_top_navigation_header_layout_and_branding(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is launched on the device.
    Steps:
        1. Observe the top navigation bar across screens.
    Expected Result:
        The top header displays the Sauce Labs logo, hamburger menu button,
        sort button, and shopping cart icon.
    """
    header = catalog_page.header

    with allure.step("Step 1: Verify Sauce Labs logo and branding in top header"):
        assert header.is_title_displayed(), "Sauce Labs logo and title is not displayed in header"

    with allure.step("Step 2: Verify hamburger menu button in top header"):
        assert header.is_displayed(header.MENU_BUTTON), (
            "Hamburger menu button is not displayed in header"
        )

    with allure.step("Step 3: Verify sort button in top header"):
        assert header.is_displayed(header.SORT_BUTTON), "Sort button is not displayed in header"

    with allure.step("Step 4: Verify shopping cart icon in top header"):
        assert header.is_displayed(header.CART_ICON) or header.is_displayed(header.CART_BUTTON), (
            "Shopping cart button or icon is not displayed in header"
        )
