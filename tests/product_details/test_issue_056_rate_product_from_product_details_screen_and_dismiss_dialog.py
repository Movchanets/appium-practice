"""Test scenario for TC-056: Rate Product from Product Details Screen and Dismiss Dialog."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.product_details
@allure.feature("Product Details")
@allure.story("Product Review")
@allure.title("TC-056: Rate Product from Product Details Screen and Dismiss Dialog")
@allure.issue("56")
def test_issue_056_rate_product_from_product_details_screen_and_dismiss_dialog(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """Preconditions:
        User is on the Product Details screen.

    Steps:
        1. Tap the 5th star icon in the product rating section.
        2. Verify the thank-you dialog appears.
        3. Tap the "Close" button.

    Expected Result:
        Review popup opens with "Thank you for submitting your review!" and closes cleanly,
        returning to the Product Details screen.
    """
    with allure.step("Precondition: User is on the Product Details screen"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        assert product_details_page.is_loaded(), "Product details page did not load"

    with allure.step("Step 1: Tap the 5th star icon in the product rating section"):
        product_details_page.click_rating_star(star=5)

    with allure.step("Step 2: Verify the thank-you dialog appears"):
        assert product_details_page.review_modal.is_displayed(), (
            "Review modal dialog is not displayed after rating"
        )
        dialog_message = product_details_page.review_modal.get_message()
        assert "Thank you for submitting your review!" in dialog_message, (
            f"Expected 'Thank you for submitting your review!', but got '{dialog_message}'"
        )

    with allure.step("Step 3: Tap the 'Close' button"):
        product_details_page.review_modal.close()

    with allure.step(
        "Expected Result: Review popup closes cleanly, returning to the Product Details screen"
    ):
        assert not product_details_page.review_modal.is_displayed(timeout=3.0), (
            "Review modal dialog did not close after tapping Close"
        )
        assert product_details_page.is_loaded(), (
            "Product Details screen is not displayed after closing review dialog"
        )
