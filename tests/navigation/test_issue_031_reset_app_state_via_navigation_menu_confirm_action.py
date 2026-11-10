"""Test scenario for resetting app state via navigation menu with confirm action."""

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
@allure.title("Reset App State via Navigation Menu - Confirm Action")
@allure.issue("31")
def test_issue_031_reset_app_state_via_navigation_menu_confirm_action(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
    confirmation_modal: ConfirmationModal,
) -> None:
    """
    Preconditions:
        User has added items to the cart or altered settings; navigation drawer is open.
    Steps:
        1. Tap "Reset App State" in the navigation drawer menu.
        2. On the confirmation popup, tap "Reset App".
    Expected Result:
        The popup closes, app state is cleared, cart badge count returns to 0,
        and user returns to the catalog.
    """
    with allure.step("Precondition: User adds an item to the cart and opens navigation drawer"):
        catalog_page.select_product_by_title("Sauce Labs Backpack")
        product_details_page.add_to_cart()
        assert catalog_page.get_cart_item_count() > 0, (
            "Cart badge count is 0 before resetting app state"
        )
        catalog_page.open_menu()

    with allure.step("Step 1: Tap 'Reset App State' in the navigation drawer menu"):
        catalog_page.drawer_menu.click_reset_app_state()

    with allure.step("Step 2: On the confirmation popup, tap 'Reset App'"):
        confirmation_modal.confirm()
        if confirmation_modal.is_displayed(timeout=2.0):
            confirmation_modal.confirm()

    with allure.step(
        "Verify popup closes, app state is cleared, cart count is 0, and user returns to catalog"
    ):
        assert not confirmation_modal.is_displayed(timeout=2.0), "Confirmation popup did not close"
        assert catalog_page.get_cart_item_count() == 0, (
            "Cart badge count is not 0 after resetting app state"
        )
        assert catalog_page.is_loaded(), "User did not return to the Catalog screen"
