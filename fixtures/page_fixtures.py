"""Page Object Model (POM) fixtures for Sauce Labs Demo App screens."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from appium import webdriver

from pages.about_page import AboutPage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_review_page import CheckoutReviewPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.drawing_page import DrawingPage
from pages.geo_location_page import GeoLocationPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
from pages.qr_code_scanner_page import QrCodeScannerPage
from pages.webview_page import WebViewPage


@pytest.fixture(scope="function")
def catalog_page(driver: webdriver.Remote) -> CatalogPage:
    """Fixture providing initialized CatalogPage instance."""
    return CatalogPage(driver)


@pytest.fixture(scope="function")
def login_page(driver: webdriver.Remote) -> Generator[LoginPage, None, None]:
    """Fixture navigating to Login screen via drawer menu and returning LoginPage."""
    page = LoginPage(driver)
    page.open_menu()
    page.drawer_menu.logout_if_logged_in()
    page.open_menu()
    page.drawer_menu.click_login()
    yield page
    try:
        page.open_menu()
        page.drawer_menu.logout_if_logged_in()
    except Exception:
        pass


@pytest.fixture(scope="function")
def product_details_page(driver: webdriver.Remote) -> ProductDetailsPage:
    """Fixture providing initialized ProductDetailsPage instance."""
    return ProductDetailsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: webdriver.Remote) -> CartPage:
    """Fixture navigating to Cart screen via header and returning CartPage."""
    page = CartPage(driver)
    page.header.click_cart()
    return page


@pytest.fixture(scope="function")
def checkout_shipping_page(driver: webdriver.Remote) -> CheckoutShippingPage:
    """Fixture providing initialized CheckoutShippingPage instance."""
    return CheckoutShippingPage(driver)


@pytest.fixture(scope="function")
def checkout_payment_page(driver: webdriver.Remote) -> CheckoutPaymentPage:
    """Fixture providing initialized CheckoutPaymentPage instance."""
    return CheckoutPaymentPage(driver)


@pytest.fixture(scope="function")
def checkout_review_page(driver: webdriver.Remote) -> CheckoutReviewPage:
    """Fixture providing initialized CheckoutReviewPage instance."""
    return CheckoutReviewPage(driver)


@pytest.fixture(scope="function")
def checkout_complete_page(driver: webdriver.Remote) -> CheckoutCompletePage:
    """Fixture providing initialized CheckoutCompletePage instance."""
    return CheckoutCompletePage(driver)


@pytest.fixture(scope="function")
def webview_page(driver: webdriver.Remote) -> WebViewPage:
    """Fixture navigating to WebView screen via drawer menu and returning WebViewPage."""
    page = WebViewPage(driver)
    page.open_menu()
    page.drawer_menu.click_webview()
    return page


@pytest.fixture(scope="function")
def qr_code_scanner_page(driver: webdriver.Remote) -> QrCodeScannerPage:
    """Fixture navigating to QR Code Scanner via drawer menu and returning QrCodeScannerPage."""
    page = QrCodeScannerPage(driver)
    page.open_menu()
    page.drawer_menu.click_qr_code_scanner()
    return page


@pytest.fixture(scope="function")
def geo_location_page(driver: webdriver.Remote) -> GeoLocationPage:
    """Fixture navigating to Geo Location screen via drawer menu and returning GeoLocationPage."""
    page = GeoLocationPage(driver)
    page.open_menu()
    page.drawer_menu.click_geo_location()
    return page


@pytest.fixture(scope="function")
def drawing_page(driver: webdriver.Remote) -> DrawingPage:
    """Fixture navigating to Drawing screen via drawer menu and returning DrawingPage."""
    page = DrawingPage(driver)
    page.open_menu()
    page.drawer_menu.click_drawing()
    return page


@pytest.fixture(scope="function")
def about_page(driver: webdriver.Remote) -> AboutPage:
    """Fixture navigating to About screen via drawer menu and returning AboutPage."""
    page = AboutPage(driver)
    page.open_menu()
    page.drawer_menu.click_about()
    return page
