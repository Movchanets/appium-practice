"""Catalog and Product Listing Page Object."""

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page Object encapsulating product grid catalog interactions and cart indicators."""

    HEADER_TITLE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Products'] | //*[@content-desc='App logo and name']",
    )
    PRODUCT_ITEMS = (
        AppiumBy.XPATH,
        "//android.view.ViewGroup[contains(@content-desc, 'store item')] "
        "| //*[@content-desc='Product Item']",
    )
    CART_BADGE = (
        AppiumBy.XPATH,
        "//*[@content-desc='View cart'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/cartIV']",
    )
    MENU_BUTTON = (
        AppiumBy.XPATH,
        "//*[@content-desc='View menu' or @content-desc='open menu'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/menuIV']",
    )
    SORT_BUTTON = (
        AppiumBy.XPATH,
        "//*[@resource-id='com.saucelabs.mydemoapp.android:id/sortIV']",
    )

    DRAWER_MENU = (
        AppiumBy.XPATH,
        "//*[@resource-id='com.saucelabs.mydemoapp.android:id/menuRV'] "
        "| //*[@resource-id='com.saucelabs.mydemoapp.android:id/drawerMenu']",
    )
    MENU_LOGIN_ITEM = (
        AppiumBy.XPATH,
        "//*[@content-desc='menu item log in' or @content-desc='Login Menu Item' "
        "or @text='Log In' or contains(@text, 'Log In')]",
    )
    MENU_LOGOUT_ITEM = (
        AppiumBy.XPATH,
        "//*[@content-desc='Logout Menu Item' or @text='Log Out' or contains(@text, 'Log Out')]",
    )
    LOGOUT_CONFIRM_BUTTON = (
        AppiumBy.XPATH,
        "//*[@resource-id='android:id/button1' or @text='LOG OUT' or @text='Log Out']",
    )
    ALERT_OK_BUTTON = (
        AppiumBy.XPATH,
        "//*[@resource-id='android:id/button1' or @text='OK' or @text='Ok']",
    )

    def is_loaded(self) -> bool:
        """Check if catalog header title is visible indicating page readiness."""
        return self.is_displayed(self.HEADER_TITLE, timeout=10.0)

    def open_menu(self) -> Self:
        """Tap navigation drawer trigger button if drawer is not already opened."""
        if not self.is_displayed(self.DRAWER_MENU, timeout=1.5):
            self.click(self.MENU_BUTTON)
        return self

    def logout_if_logged_in(self) -> Self:
        """Perform graceful logout if an active user session is present in the navigation drawer."""
        self.open_menu()
        if self.is_displayed(self.MENU_LOGOUT_ITEM, timeout=2.0):
            self.click(self.MENU_LOGOUT_ITEM)
            if self.is_displayed(self.LOGOUT_CONFIRM_BUTTON, timeout=3.0):
                self.click(self.LOGOUT_CONFIRM_BUTTON)
            if self.is_displayed(self.ALERT_OK_BUTTON, timeout=3.0):
                self.click(self.ALERT_OK_BUTTON)
        return self

    def navigate_to_login(self) -> Self:
        """Open slide menu and navigate to Login screen, logging out first if session active."""
        self.logout_if_logged_in()
        self.open_menu()
        self.click(self.MENU_LOGIN_ITEM)
        return self

    def select_product_by_title(self, title: str) -> Self:
        """Scroll dynamically to find the specified product title and tap it."""
        self.scroll_to_text(title)
        product_locator = (
            AppiumBy.XPATH,
            f"//android.widget.TextView[@text='{title}']",
        )
        self.click(product_locator)
        return self

    def scroll_catalog_down(self) -> Self:
        """Perform a dynamic swipe up to scroll catalog down."""
        self.swipe_up()
        return self

    def get_cart_item_count(self) -> int:
        """Extract number of items displayed in cart badge; returns 0 if absent."""
        if not self.is_displayed(self.CART_BADGE, timeout=2.0):
            return 0
        raw_text = self.get_text(self.CART_BADGE, timeout=2.0)
        try:
            return int(raw_text.strip())
        except ValueError:
            return 0
