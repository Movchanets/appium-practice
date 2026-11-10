"""Practical coding exercises and debugging trainer for Mobile ATQC candidates.

This module contains:
- 4 Hands-on Tasks (marked with # TODO:) designed for interview practice.
- 2 Intentionally Broken Tests for logcat and screenshot debugging training.
"""

import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.components.header_component import HeaderComponent
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage


# ============================================================================
# TASK 1: POM / COM Architecture & Component Interaction
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_1_verify_header_and_catalog_components(
    catalog_page: CatalogPage,
    header_component: HeaderComponent,
) -> None:
    """ЗАВДАННЯ 1: Перевірка компонентів HeaderComponent та ProductCardComponent.

    Усі локатори мають зберігатися виключно у змінних класів POM/COM.
    """
    pytest.skip("Практичне завдання 1: Прибери skip для перевірки компонентів каталогу")

    assert header_component.is_title_displayed(), "Header logo should be visible"
    cards = catalog_page.get_product_cards()
    assert len(cards) > 0, "Catalog should render product cards"


# ============================================================================
# TASK 2: Boundary Value Analysis (BVA) & Equivalence Partitioning Test
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
@pytest.mark.parametrize(
    ("username", "password", "expected_error_contains"),
    [
        ("", "secret_password", "Username is required"),
    ],
)
def test_task_2_bva_login_validation(
    catalog_page: CatalogPage,
    login_page: LoginPage,
    username: str,
    password: str,
    expected_error_contains: str,
) -> None:
    """ЗАВДАННЯ 2: Параметризований тест валідації полів за технікою BVA/EP."""
    catalog_page.navigate_to_login()
    login_page.login(username=username, password=password)

    assert login_page.is_error_displayed(), "Помилка валідації має бути видима"
    error_text = login_page.get_error_message()
    assert expected_error_contains in error_text, f"Очікували '{expected_error_contains}' в помилці"


# ============================================================================
# TASK 3: Screen Orientation Lifecycle & State Preservation
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_3_screen_orientation_state_preservation(
    catalog_page: CatalogPage,
    login_page: LoginPage,
) -> None:
    """ЗАВДАННЯ 3: Перевірка збереження даних форми при повороті екрана."""
    pytest.skip("Практичне завдання 3: Реалізуй поворот екрана та перевірку збереження стану")

    catalog_page.navigate_to_login()
    test_user = "tactical_operator"
    login_page.enter_username(test_user)

    try:
        login_page.set_orientation("LANDSCAPE")
        assert login_page.is_loaded(), "Екран логіну має залишатися доступним після повороту"
    finally:
        login_page.set_orientation("PORTRAIT")


# ============================================================================
# TASK 4: Refactor Anti-Pattern Test (Flaky -> Production-Grade)
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_4_refactor_anti_pattern_test(catalog_page: CatalogPage) -> None:
    """ЗАВДАННЯ 4: Рефакторинг антипатернів (явні очікування та W3C жести)."""
    assert catalog_page.is_loaded()
    catalog_page.swipe_up()
    assert catalog_page.is_loaded()


# ============================================================================
# DEBUGGING TRAINER: 2 Intentionally Broken Tests for Failure Diagnosis
# ============================================================================
@pytest.mark.mobile
@pytest.mark.debug_trainer
def test_debug_task_1_intentional_unopened_screen_element(
    product_details_page: ProductDetailsPage,
) -> None:
    """ТРЕНАЖЕР ДЕБАГУ 1: Спроба взаємодії з елементом ProductDetailsPage без переходу на екран."""
    product_details_page.add_to_cart()


@pytest.mark.mobile
@pytest.mark.debug_trainer
def test_debug_task_2_intentional_state_mismatch(cart_page: CartPage) -> None:
    """ТРЕНАЖЕР ДЕБАГУ 2: Спроба натиснути Checkout без відкриття кошика з товарами."""
    cart_page.proceed_to_checkout()
