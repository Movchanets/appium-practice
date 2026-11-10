"""Page Object Model (POM), Component Object Model (COM), and Modals package."""

from pages.about_page import AboutPage
from pages.base import Base
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_review_page import CheckoutReviewPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.components.base_component import BaseComponent
from pages.components.cart_item_component import CartItemComponent
from pages.components.drawer_menu_component import DrawerMenuComponent
from pages.components.footer_component import FooterComponent
from pages.components.header_component import HeaderComponent
from pages.components.product_card_component import ProductCardComponent
from pages.drawing_page import DrawingPage
from pages.geo_location_page import GeoLocationPage
from pages.login_page import LoginPage
from pages.modals.base_modal import BaseModal
from pages.modals.confirmation_modal import ConfirmationModal
from pages.modals.review_modal import ReviewModal
from pages.modals.sort_modal import SortModal
from pages.product_details_page import ProductDetailsPage
from pages.qr_code_scanner_page import QrCodeScannerPage
from pages.types import Locator, ProductColor, ScreenOrientation, SortOption, SwipeDirection
from pages.webview_page import WebViewPage

__all__ = [
    "AboutPage",
    "Base",
    "BaseComponent",
    "BaseModal",
    "BasePage",
    "CartItemComponent",
    "CartPage",
    "CatalogPage",
    "CheckoutCompletePage",
    "CheckoutPaymentPage",
    "CheckoutReviewPage",
    "CheckoutShippingPage",
    "ConfirmationModal",
    "DrawerMenuComponent",
    "DrawingPage",
    "FooterComponent",
    "GeoLocationPage",
    "HeaderComponent",
    "Locator",
    "LoginPage",
    "ProductCardComponent",
    "ProductColor",
    "ProductDetailsPage",
    "QrCodeScannerPage",
    "ReviewModal",
    "ScreenOrientation",
    "SortModal",
    "SortOption",
    "SwipeDirection",
    "WebViewPage",
]
