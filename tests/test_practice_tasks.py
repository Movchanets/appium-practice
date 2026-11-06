"""Practical coding exercises and debugging trainer for Mobile ATQC candidates.

This module contains:
- 4 Hands-on Tasks (marked with # TODO:) designed for interview practice.
- 2 Intentionally Broken Tests for logcat and screenshot debugging training.
"""

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from pages.base_page import BasePage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


# ============================================================================
# TASK 1: Locator Architecture & Refactoring (ACCESSIBILITY_ID & relative XPATH)
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_1_fix_brittle_locators(driver: WebDriver) -> None:
    """ЗАВДАННЯ 1: Заміна крихких локаторів на стійкі.

    Проблема:
    Абсолютні шляхи (наприклад, /hierarchy/android.widget.FrameLayout/...) ламаються
    при найменшій зміні верстки Android або на іншому розмірі екрана.

    Твоє завдання (# TODO):
    1. Заміни BRITTLE_CART_LOCATOR на стабільний AppiumBy.ACCESSIBILITY_ID або AppiumBy.ID.
    2. Заміни BRITTLE_TITLE_LOCATOR на стійкий відносний AppiumBy.XPATH.
    3. Прибери pytest.skip() після завершення.
    """
    pytest.skip("Практичне завдання 1: Прибери skip після заміни локаторів на стабільні")

    base = BasePage(driver)

    # ❌ АНТИПАТЕРН: Крихкі абсолютні локатори:
    # BRITTLE_CART_LOCATOR = (
    #     AppiumBy.XPATH,
    #     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
    #     "android.widget.FrameLayout/android.widget.LinearLayout/"
    #     "android.widget.FrameLayout/android.view.ViewGroup/"
    #     "android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]",
    # )

    # TODO: Реалізуй стійкі локатори відповідно до правил CLAUDE.md:
    STABLE_CART_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "cart badge")  # Доопрацюй за потреби
    STABLE_TITLE_LOCATOR = (AppiumBy.XPATH, "//android.widget.TextView[@text='Products']")

    cart_elem = base.find_element(STABLE_CART_LOCATOR)
    title_elem = base.find_element(STABLE_TITLE_LOCATOR)

    assert cart_elem.is_displayed(), "Cart icon should be found via stable locator"
    assert "Products" in title_elem.text, "Title should be verified via relative XPath"


# ============================================================================
# TASK 2: Boundary Value Analysis (BVA) & Equivalence Partitioning Test
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
# TODO: Додай параметризацію @pytest.mark.parametrize для перевірки граничних значень (BVA)
# Перевір:
# 1. Порожній рядок (Empty: "") -> очікується валідаційна помилка "Username is required"
# 2. 1 символ (Нижче мінімальної довжини) -> очікується помилка довжини
# 3. Довгий рядок (Overflow boundary: 100+ символів) -> очікується коректна обробка
@pytest.mark.parametrize(
    ("username", "password", "expected_error_contains"),
    [
        ("", "secret_password", "Username is required"),
        # TODO: Додай кейси для BVA (1 char, boundary lengths)
    ],
)
def test_task_2_bva_login_validation(
    driver: WebDriver, username: str, password: str, expected_error_contains: str
) -> None:
    """ЗАВДАННЯ 2: Параметризований тест валідації полів за технікою BVA/EP."""
    catalog = CatalogPage(driver)
    catalog.open_menu()

    login_page = LoginPage(driver)
    login_page.login(username=username, password=password)

    # TODO: Перевір відображення повідомлення про помилку та відповідність тексту
    assert login_page.is_error_displayed(), "Помилка валідації має бути видима"
    error_text = login_page.get_error_message()
    assert expected_error_contains in error_text, f"Очікували '{expected_error_contains}' в помилці"


# ============================================================================
# TASK 3: Screen Orientation Lifecycle & State Preservation
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_3_screen_orientation_state_preservation(driver: WebDriver) -> None:
    """ЗАВДАННЯ 3: Перевірка збереження даних форми при повороті екрана.

    Мобільна специфіка:
    При зміні орієнтації Android Activity за замовчуванням знищується (onDestroy)
    та створюється заново (onCreate). Якщо розробник не зберіг стан (onSaveInstanceState),
    усі введені користувачем дані буде стерто!

    Твоє завдання (# TODO):
    1. Відкрий екран логіну.
    2. Введи текст у поле Username: 'tactical_operator'.
    3. Зміни орієнтацію на LANDSCAPE через BasePage.set_orientation().
    4. Перевір, що введений текст зберігся у полі.
    5. Поверни орієнтацію назад на PORTRAIT (обов'язковий teardown).
    """
    pytest.skip("Практичне завдання 3: Реалізуй поворот екрана та перевірку збереження стану")

    catalog = CatalogPage(driver)
    catalog.open_menu()
    login_page = LoginPage(driver)

    test_user = "tactical_operator"
    login_page.enter_username(test_user)

    try:
        # TODO: Зміни орієнтацію на LANDSCAPE
        login_page.set_orientation("LANDSCAPE")

        # TODO: Знайди поле знову та отримай текст:
        # field = login_page.find_element(login_page.USERNAME_INPUT)
        # assert field.text == test_user, "Дані форми мають зберігатись при перевороті екрана"
        pass
    finally:
        # Обов'язково повертаємо девайс у стандартне положення для наступних тестів
        login_page.set_orientation("PORTRAIT")


# ============================================================================
# TASK 4: Refactor Anti-Pattern Test (Flaky -> Production-Grade)
# ============================================================================
@pytest.mark.mobile
@pytest.mark.practice
def test_task_4_refactor_anti_pattern_test(driver: WebDriver) -> None:
    """ЗАВДАННЯ 4: Рефакторинг антипатернів.

    Знайди та виправ у коді нижче:
    1. Жорсткі затримки time.sleep() -> замінити на явні очікування WebDriverWait.
    2. Хардкод пікселів (x=350, y=820) -> замінити на динамічні відсотки від розміру екрана.
    3. Відсутність Page Object Model -> винести локатори та логіку в сторінку.
    """
    # ❌ ПОГАНИЙ КОД (Anti-Pattern):
    # import time
    # time.sleep(5)
    # driver.tap([(350, 820)])  # Хардкод пікселів! Зламається на іншому девайсі
    # time.sleep(3)
    # elem = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/...")
    # assert elem.is_displayed()

    # TODO: Реалізуй чисту версію за допомогою BasePage/CatalogPage:
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()
    # Використовуй dynamic swipe або tap_by_coordinates(0.5, 0.8)
    catalog.swipe_up()
    assert catalog.is_loaded()


# ============================================================================
# DEBUGGING TRAINER: 2 Intentionally Broken Tests for Failure Diagnosis
# ============================================================================
@pytest.mark.mobile
@pytest.mark.debug_trainer
def test_debug_task_1_intentional_broken_locator(driver: WebDriver) -> None:
    """ТРЕНАЖЕР ДЕБАГУ 1: Падіння через неіснуючий локатор.

    Мета вправи:
    1. Запустити цей тест: pytest tests/test_practice_tasks.py -k broken_locator
    2. Побачити автоматичне створення скріншота в artifacts/screenshots/
    3. Відкрити XML-дамп у artifacts/page_sources/ і знайти правильний Accessibility ID.
    4. Виправити локатор нижче, щоб тест пройшов.
    """
    base = BasePage(driver)
    # ❌ НАВМИСНА ПОМИЛКА: такого accessibility_id не існує
    WRONG_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "non_existent_inventory_button_12345")
    element = base.find_element(WRONG_LOCATOR, timeout=3.0)
    assert element.is_displayed()


@pytest.mark.mobile
@pytest.mark.debug_trainer
def test_debug_task_2_intentional_state_mismatch(driver: WebDriver) -> None:
    """ТРЕНАЖЕР ДЕБАГУ 2: Падіння через невідповідність стану додатка / timing.

    Мета вправи:
    1. Запустити: pytest tests/test_practice_tasks.py -k state_mismatch
    2. Перевірити збережені логи artifacts/logs/*_logcat.log
    3. Зрозуміти, чому кнопка 'Checkout' недоступна на головному екрані без товарів у кошику.
    """
    base = BasePage(driver)
    # ❌ НАВМИСНА ПОМИЛКА: Спроба знайти кнопку чекауту на екрані каталогу без додавання товару
    CHECKOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Checkout button")
    checkout_element = base.find_element(CHECKOUT_BUTTON, timeout=3.0)
    assert checkout_element.is_displayed(), "Checkout button should be present"
