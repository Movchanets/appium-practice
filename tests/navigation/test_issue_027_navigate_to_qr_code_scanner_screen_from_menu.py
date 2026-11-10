"""Test scenario for Issue 027: Navigate to QR Code Scanner Screen from Menu."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.qr_code_scanner_page import QrCodeScannerPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Drawer Menu Navigation")
@allure.title("Navigate to QR Code Scanner Screen from Menu")
def test_issue_027_navigate_to_qr_code_scanner_screen_from_menu(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Navigation drawer menu is open.
    Steps:
        1. Tap "QR Code Scanner" in the navigation menu.
    Expected Result:
        The QR Code Scanner screen opens displaying the camera scanning viewfinder.
    """
    with allure.step("Precondition: Open navigation drawer menu"):
        catalog_page.open_menu()
        assert catalog_page.is_displayed(catalog_page.DRAWER_MENU), (
            "Navigation drawer menu is not open"
        )

    with allure.step("Step 1: Tap 'QR Code Scanner' in the navigation menu"):
        catalog_page.drawer_menu.click_qr_code_scanner()

    with allure.step("Verify: QR Code Scanner screen opens"):
        scanner_page = QrCodeScannerPage(catalog_page.driver)
        scanner_page.handle_permission_alert(allow=True)
        assert scanner_page.is_loaded(), "QR Code Scanner screen is not loaded"
        assert "QR Code Scanner" in scanner_page.get_title_text(), (
            f"Unexpected QR Code Scanner title: {scanner_page.get_title_text()}"
        )
