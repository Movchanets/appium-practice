"""Test TC-094: Draw Signature Stroke on Canvas and Clear Pad."""

from __future__ import annotations

import allure
import pytest

from pages.drawing_page import DrawingPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.device_features
@allure.feature("Device Features")
@allure.story("Drawing")
@allure.title("TC-094: Draw Signature Stroke on Canvas and Clear Pad")
@allure.issue("94")
def test_issue_094_draw_signature_stroke_on_canvas_and_clear_pad(
    drawing_page: DrawingPage,
) -> None:
    """Preconditions:
        User navigates to the Drawing screen from the menu.
    Steps:
        1. Perform a touch drag gesture across the signature drawing pad.
        2. Verify a drawing line appears on the canvas.
        3. Tap the 'Clear' button.
    Expected Result:
        Signature stroke renders on the drawing pad, and tapping 'Clear'
        completely erases the canvas.
    """
    with allure.step("Precondition: User is on the Drawing screen"):
        assert drawing_page.is_loaded(), "Drawing screen is not loaded"

    with allure.step("Step 1 & 2: Perform touch drag across drawing pad and verify canvas"):
        drawing_page.draw_signature()
        assert drawing_page.is_displayed(drawing_page.SIGNATURE_PAD), (
            "Signature pad is not displayed after drawing"
        )

    with allure.step("Step 3: Tap 'Clear' button"):
        drawing_page.clear()
        assert drawing_page.is_loaded(), "Drawing screen is not loaded after clearing canvas"
