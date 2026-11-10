"""Modal Dialog fixtures for system and custom application popups."""

from __future__ import annotations

import pytest
from appium import webdriver

from pages.modals.confirmation_modal import ConfirmationModal
from pages.modals.review_modal import ReviewModal
from pages.modals.sort_modal import SortModal


@pytest.fixture(scope="function")
def confirmation_modal(driver: webdriver.Remote) -> ConfirmationModal:
    """Fixture providing initialized ConfirmationModal instance."""
    return ConfirmationModal(driver)


@pytest.fixture(scope="function")
def sort_modal(driver: webdriver.Remote) -> SortModal:
    """Fixture providing initialized SortModal instance."""
    return SortModal(driver)


@pytest.fixture(scope="function")
def review_modal(driver: webdriver.Remote) -> ReviewModal:
    """Fixture providing initialized ReviewModal instance."""
    return ReviewModal(driver)
