"""Test scenario for Issue 024: Verify Shopping Cart Badge is Empty by Default."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.navigation
@allure.feature("Navigation")
@allure.story("Shopping Cart Badge")
@allure.title("Verify Shopping Cart Badge is Empty by Default")
def test_issue_024_verify_shopping_cart_badge_is_empty_by_default(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        Fresh app start with no items added to the cart.
    Steps:
        1. Inspect the shopping cart icon in the top-right header.
    Expected Result:
        No badge count or a count of 0 is displayed on the shopping cart icon.
    """
    with allure.step("Step 1: Inspect the shopping cart icon in the top-right header"):
        badge_count = catalog_page.get_cart_item_count()
        assert badge_count == 0, f"Expected empty shopping cart count of 0, but found {badge_count}"

        badge_displayed = catalog_page.header.is_displayed(
            catalog_page.header.CART_BADGE, timeout=2.0
        )
        if badge_displayed:
            badge_text = catalog_page.header.get_text(
                catalog_page.header.CART_BADGE, timeout=2.0
            ).strip()
            assert badge_text in ("0", ""), (
                f"Expected cart badge text to be '0' or empty, but got '{badge_text}'"
            )
