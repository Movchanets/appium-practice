"""Test TC-098: Verify Smooth Touch Gestures Swipe and Long Press."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.gestures_lifecycle
@allure.feature("Gestures & Lifecycle")
@allure.story("Touch Gestures")
@allure.title("TC-098: Verify Smooth Touch Gestures Swipe and Long Press")
@allure.issue("98")
def test_issue_098_verify_smooth_touch_gestures_swipe_and_long_press(
    catalog_page: CatalogPage,
) -> None:
    """Preconditions:
        App is on the Catalog screen.
    Steps:
        1. Swipe upward to scroll down through the catalog.
        2. Swipe downward to scroll back to the top.
        3. Perform a touch-and-hold (long press) gesture on a product card.
    Expected Result:
        All touch gestures execute smoothly and the catalog responds without
        jitter or accidental clicks.
    """
    with allure.step("Precondition: App is on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog screen is not loaded"

    with allure.step("Step 1: Swipe upward to scroll down through the catalog"):
        catalog_page.swipe_up()
        assert catalog_page.is_loaded(), "Catalog screen is not loaded after swiping up"

    with allure.step("Step 2: Swipe downward to scroll back to the top"):
        catalog_page.swipe_down()
        assert catalog_page.is_loaded(), "Catalog screen is not loaded after swiping down"

    with allure.step("Step 3: Perform a touch-and-hold (long press) gesture on a product card"):
        catalog_page.long_press(catalog_page.PRODUCT_ITEMS, duration_s=1.5)
        assert catalog_page.is_loaded(), "Catalog screen is not loaded after long press gesture"
