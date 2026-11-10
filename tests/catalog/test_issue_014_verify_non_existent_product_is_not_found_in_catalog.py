"""Test scenario for verifying non-existent product is not found in catalog."""

import allure
import pytest
from selenium.common.exceptions import NoSuchElementException

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Catalog Screen")
@allure.story("Product Search")
@allure.title("Verify Non-Existent Product is Not Found in Catalog")
def test_issue_014_verify_non_existent_product_is_not_found_in_catalog(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Scroll through the catalog searching for a non-existent item named
           "Non-Existent Super Gizmo".
    Expected Result:
        The non-existent product does not appear anywhere in the catalog list.
    """
    target_product = "Non-Existent Super Gizmo"

    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step(
        f"Step 1: Scroll through the catalog searching for non-existent item '{target_product}'"
    ):
        with pytest.raises(NoSuchElementException):
            catalog_page.scroll_to_text(target_product, max_swipes=3)

    with allure.step(f"Verify non-existent product '{target_product}' is not displayed"):
        visible_cards = catalog_page.get_product_cards()
        for card in visible_cards:
            assert target_product not in card.get_title(), (
                f"Unexpectedly found '{target_product}' in catalog"
            )
