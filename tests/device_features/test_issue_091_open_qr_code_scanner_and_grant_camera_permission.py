"""Test TC-091: Open QR Code Scanner and Grant Camera Permission."""

from __future__ import annotations

import allure
import pytest

from pages.qr_code_scanner_page import QrCodeScannerPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.device_features
@allure.feature("Device Features")
@allure.story("QR Code Scanner")
@allure.title("TC-091: Open QR Code Scanner and Grant Camera Permission")
@allure.issue("91")
def test_issue_091_open_qr_code_scanner_and_grant_camera_permission(
    qr_code_scanner_page: QrCodeScannerPage,
) -> None:
    """Preconditions:
        User navigates to QR Code Scanner from the menu.
    Steps:
        1. When the system camera permission dialog appears, tap 'Allow'.
        2. Observe the QR Code Scanner screen.
    Expected Result:
        Camera permission is granted, and the QR Code Scanner viewfinder opens
        with title 'QR Code Scanner'.
    """
    with allure.step("Step 1: When system camera permission appears, tap Allow"):
        qr_code_scanner_page.handle_permission_alert(allow=True)

    with allure.step("Step 2: Observe the QR Code Scanner screen"):
        assert qr_code_scanner_page.is_loaded(), "QR Code Scanner screen is not loaded"
        assert "QR Code Scanner" in qr_code_scanner_page.get_title_text(), (
            f"Unexpected title text: '{qr_code_scanner_page.get_title_text()}'"
        )
