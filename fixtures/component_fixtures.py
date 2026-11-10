"""Component Object Model (COM) fixtures for shared UI components."""

from __future__ import annotations

import pytest

from pages.catalog_page import CatalogPage
from pages.components.drawer_menu_component import DrawerMenuComponent
from pages.components.footer_component import FooterComponent
from pages.components.header_component import HeaderComponent


@pytest.fixture(scope="function")
def header_component(catalog_page: CatalogPage) -> HeaderComponent:
    """Fixture providing HeaderComponent instance bound to active screen."""
    return catalog_page.header


@pytest.fixture(scope="function")
def drawer_menu_component(catalog_page: CatalogPage) -> DrawerMenuComponent:
    """Fixture providing DrawerMenuComponent instance bound to active screen."""
    return catalog_page.drawer_menu


@pytest.fixture(scope="function")
def footer_component(catalog_page: CatalogPage) -> FooterComponent:
    """Fixture providing FooterComponent instance bound to active catalog screen."""
    return catalog_page.footer
