"""Catalog and Product Listing Page Object."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import BasePage
from pages.components.footer_component import FooterComponent
from pages.components.product_card_component import ProductCardComponent
from pages.modals.confirmation_modal import ConfirmationModal
from pages.modals.review_modal import ReviewModal
from pages.modals.sort_modal import SortModal
from pages.types import Locator, SortOption


class CatalogPage(BasePage):
    """Page Object encapsulating product grid catalog interactions and composed components."""

    PRODUCT_ITEMS: Locator = (
        AppiumBy.XPATH,
        '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.saucelabs.mydemoapp.android:id/productRV"]/android.view.ViewGroup',
    )
    SORT_BUTTON: Locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortIV")
    FOOTER_ROOT: Locator = (
        AppiumBy.XPATH,
        '//android.widget.TextView[contains(@text, "Sauce Labs All Rights Reserved")]',
    )

    # ---------------------------------------------------------
    # Composed Modals
    # ---------------------------------------------------------

    @property
    def sort_modal(self) -> SortModal:
        """Access the catalog SortModal dialog."""
        return SortModal(self.driver)

    @property
    def review_modal(self) -> ReviewModal:
        """Access the ReviewModal dialog."""
        return ReviewModal(self.driver)

    @property
    def confirmation_modal(self) -> ConfirmationModal:
        """Access the standard ConfirmationModal dialog."""
        return ConfirmationModal(self.driver)

    @property
    def footer(self) -> FooterComponent:
        """Access the FooterComponent, scrolling down if needed."""
        self.scroll_to_text("Sauce Labs All Rights Reserved")
        footer_el = self.find_element(self.FOOTER_ROOT)
        return FooterComponent(footer_el)

    # ---------------------------------------------------------
    # Product Card Components
    # ---------------------------------------------------------

    def get_product_cards(self) -> list[ProductCardComponent]:
        """Return all rendered product card components on screen."""
        card_elements = self.find_elements(self.PRODUCT_ITEMS)
        return [ProductCardComponent(el) for el in card_elements]

    def get_product_card_by_title(self, title: str) -> ProductCardComponent:
        """Find a product card component by its visible title."""
        for card in self.get_product_cards():
            if title in card.get_title():
                return card
        raise NoSuchElementException(f"Product card with title '{title}' not found on screen")

    # ---------------------------------------------------------
    # Page Actions & Workflows
    # ---------------------------------------------------------

    def is_loaded(self) -> bool:
        """Check if catalog is loaded and header logo is visible."""
        return self.header.is_title_displayed(timeout=10.0)

    def logout_if_logged_in(self) -> Self:
        """Perform graceful logout if an active user session is present in the navigation drawer."""
        self.open_menu()
        self.drawer_menu.logout_if_logged_in()
        return self

    def navigate_to_login(self) -> Self:
        """Open slide menu and navigate to Login screen, logging out first if session active."""
        self.logout_if_logged_in()
        self.open_menu()
        self.drawer_menu.click_login()
        return self

    def navigate_to_cart(self) -> Self:
        """Tap header shopping cart button."""
        self.header.click_cart()
        return self

    def select_product_by_title(self, title: str) -> Self:
        """Scroll dynamically to find the specified product title and tap its card."""
        self.scroll_to_text(title)
        self.get_product_card_by_title(title).click_item()
        return self

    def sort_products(self, option: SortOption) -> Self:
        """Open sort modal and select sorting criteria."""
        self.header.click_sort()
        self.sort_modal.select_option(option)
        return self

    def scroll_catalog_down(self) -> Self:
        """Perform a dynamic swipe up to scroll catalog down."""
        self.swipe_up()
        return self

    def scroll_catalog_up(self) -> Self:
        """Perform a dynamic swipe down to scroll catalog back up to the top."""
        self.swipe_down()
        return self

    def get_footer_copyright_text(self) -> str:
        """Scroll to bottom and retrieve footer copyright banner text."""
        return self.footer.get_copyright_text()

    def get_cart_item_count(self) -> int:
        """Extract number of items displayed in cart badge; returns 0 if absent."""
        return self.header.get_cart_item_count()
