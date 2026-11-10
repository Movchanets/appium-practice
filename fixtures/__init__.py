"""Pytest fixtures package for Mobile ATQC Bootcamp."""

from fixtures.component_fixtures import (
    drawer_menu_component,
    footer_component,
    header_component,
)
from fixtures.driver_fixtures import driver
from fixtures.modal_fixtures import confirmation_modal, review_modal, sort_modal
from fixtures.page_fixtures import (
    about_page,
    cart_page,
    catalog_page,
    checkout_complete_page,
    checkout_payment_page,
    checkout_review_page,
    checkout_shipping_page,
    drawing_page,
    geo_location_page,
    login_page,
    product_details_page,
    qr_code_scanner_page,
    webview_page,
)

__all__ = [
    "about_page",
    "cart_page",
    "catalog_page",
    "checkout_complete_page",
    "checkout_payment_page",
    "checkout_review_page",
    "checkout_shipping_page",
    "confirmation_modal",
    "drawer_menu_component",
    "drawing_page",
    "driver",
    "footer_component",
    "geo_location_page",
    "header_component",
    "login_page",
    "product_details_page",
    "qr_code_scanner_page",
    "review_modal",
    "sort_modal",
    "webview_page",
]
