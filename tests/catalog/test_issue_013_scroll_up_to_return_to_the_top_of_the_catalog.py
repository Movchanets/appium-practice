"""Test scenario for scrolling up to return to the top of the catalog."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Catalog Screen")
@allure.story("Navigation Gestures")
@allure.title("Scroll Up to Return to the Top of the Catalog")
@allure.issue("13")
def test_issue_013_scroll_up_to_return_to_the_top_of_the_catalog(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is on the Catalog screen and has been scrolled down toward the bottom.
    Steps:
        1. Swipe downwards on the screen to scroll up.
        2. Observe the visible products.
    Expected Result:
        The catalog scrolls up smoothly and the initial top products
        (such as "Sauce Labs Backpack") reappear at the top.
    """
    with allure.step("Precondition: App is on Catalog screen and scrolled down toward the bottom"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"
        catalog_page.scroll_catalog_down()

    with allure.step("Step 1: Swipe downwards on the screen to scroll up"):
        catalog_page.swipe_down()

    with allure.step("Step 2: Observe the visible products"):
        backpack_card = catalog_page.get_product_card_by_title("Sauce Labs Backpack")
        assert backpack_card.is_visible(), (
            "Sauce Labs Backpack is not visible after scrolling back to top"
        )
