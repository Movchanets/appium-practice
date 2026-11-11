"""TC-004: Open Product Details by Tapping Product Title."""

from __future__ import annotations

import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@pytest.mark.xfail(
    reason=(
        "BUG: Product title TextView (titleTV) on catalog cards does not have an "
        "OnClickListener attached"
    ),
    strict=False,
)
@allure.feature("Product Catalog")
@allure.story("Product Navigation")
@allure.title("TC-004: Open Product Details by Tapping Product Title")
@allure.issue("4")
def test_issue_004_open_product_details_by_tapping_product_title(
    catalog_page: CatalogPage,
    product_details_page: ProductDetailsPage,
) -> None:
    """
    Preconditions:
        - App is open on the Catalog screen.

    Steps:
        1. Locate the item "Sauce Labs Backpack".
        2. Tap directly on the product title text.

    Expected Result:
        - The Product Details screen opens displaying "Sauce Labs Backpack" with full description,
          image, and options.
    """
    with allure.step("Precondition: Ensure Catalog page is loaded"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Locate the item 'Sauce Labs Backpack'"):
        card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        assert card.is_visible(), "Sauce Labs Backpack card is not visible"

    with allure.step("Step 2: Tap directly on the product title text"):
        card.click(card.TITLE)

    with allure.step("Verify Product Details screen opens with title, price, and options"):
        assert product_details_page.is_loaded(), "Product Details screen failed to load"
        assert product_details_page.get_title() == "Sauce Labs Backpack"
        assert product_details_page.is_displayed(product_details_page.PRODUCT_IMAGE)
        assert product_details_page.get_price() == "$ 29.99"
        assert product_details_page.get_description(), "Product description is empty"
        assert product_details_page.is_displayed(product_details_page.ADD_TO_CART_BUTTON)
