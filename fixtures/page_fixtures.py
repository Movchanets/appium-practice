"""Page Object Model (POM) fixtures for Sauce Labs Demo App screens."""

from __future__ import annotations

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
def login_page(driver: webdriver.Remote) -> LoginPage:
    """Fixture providing initialized LoginPage instance."""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def product_details_page(driver: webdriver.Remote) -> ProductDetailsPage:
    """Fixture providing initialized ProductDetailsPage instance."""
    return ProductDetailsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: webdriver.Remote) -> CartPage:
    """Fixture providing initialized CartPage instance."""
    return CartPage(driver)


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
    """Fixture providing initialized WebViewPage instance."""
    return WebViewPage(driver)


@pytest.fixture(scope="function")
def qr_code_scanner_page(driver: webdriver.Remote) -> QrCodeScannerPage:
    """Fixture providing initialized QrCodeScannerPage instance."""
    return QrCodeScannerPage(driver)


@pytest.fixture(scope="function")
def geo_location_page(driver: webdriver.Remote) -> GeoLocationPage:
    """Fixture providing initialized GeoLocationPage instance."""
    return GeoLocationPage(driver)


@pytest.fixture(scope="function")
def drawing_page(driver: webdriver.Remote) -> DrawingPage:
    """Fixture providing initialized DrawingPage instance."""
    return DrawingPage(driver)


@pytest.fixture(scope="function")
def about_page(driver: webdriver.Remote) -> AboutPage:
    """Fixture providing initialized AboutPage instance."""
    return AboutPage(driver)
