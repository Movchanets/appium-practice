"""Test scenario for verifying footer copyright banner at the bottom of the catalog."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.catalog
@allure.feature("Catalog Screen")
@allure.story("Footer Banner")
@allure.title("Verify Footer Copyright Banner at Bottom of Catalog")
@allure.issue("11")
def test_issue_011_verify_footer_copyright_banner_at_bottom_of_catalog(
    catalog_page: CatalogPage,
) -> None:
    """
    Preconditions:
        App is open on the Catalog screen.
    Steps:
        1. Scroll down to the very bottom of the catalog grid.
        2. Observe the footer banner below the last product row.
    Expected Result:
        The footer banner is displayed and contains the text: "Sauce Labs All Rights Reserved".
    """
    with allure.step("Precondition: App is open on the Catalog screen"):
        assert catalog_page.is_loaded(), "Catalog page is not loaded"

    with allure.step("Step 1: Scroll down to the very bottom of the catalog grid"):
        catalog_page.scroll_to_text("Sauce Labs All Rights Reserved")

    with allure.step("Step 2: Observe the footer banner below the last product row"):
        footer = catalog_page.footer
        assert footer.is_displayed(), "Footer banner is not displayed"
        copyright_text = footer.get_copyright_text()
        assert "Sauce Labs All Rights Reserved" in copyright_text, (
            f"Expected copyright text not found in footer: '{copyright_text}'"
        )
