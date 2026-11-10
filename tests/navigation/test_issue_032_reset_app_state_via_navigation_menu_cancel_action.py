"""Test scenario for resetting app state via navigation menu with cancel action."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.modals.confirmation_modal import ConfirmationModal
from pages.product_details_page import ProductDetailsPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.navigation
@allure.feature("Navigation Drawer")
@allure.story("Reset App State")
@allure.title("Reset App State via Navigation Menu - Cancel Action")
def test_issue_032_reset_app_state_via_navigation_menu_cancel_action(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    confirmation_modal: ConfirmationModal,
) -> None:
    """
    Preconditions:
        Reset App State confirmation dialog is open.
    Steps:
        1. Tap "Cancel" on the confirmation popup.
    Expected Result:
        The popup closes without resetting any data; items in the cart
        and current state remain unchanged.
    """
    with allure.step("Precondition: User adds item to cart and opens Reset App State dialog"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        initial_cart_count = catalog_page.get_cart_item_count()
        assert initial_cart_count > 0, "Cart should contain items prior to cancel test"
        catalog_page.open_menu()
        catalog_page.drawer_menu.click_reset_app_state()
        assert confirmation_modal.is_displayed(), "Confirmation dialog is not displayed"

    with allure.step("Step 1: Tap 'Cancel' on the confirmation popup"):
        confirmation_modal.dismiss()

    with allure.step("Verify popup closes without resetting data and cart count remains unchanged"):
        assert not confirmation_modal.is_displayed(timeout=2.0), "Confirmation popup did not close"
        assert catalog_page.get_cart_item_count() == initial_cart_count, (
            "Cart count changed after canceling reset"
        )
