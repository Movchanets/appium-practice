"""Base Page Object implementation providing core actions, waits, and W3C gestures."""

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[AppiumBy | str, str]


class BasePage:
    """Foundational Page Object with robust explicit waits and dynamic W3C touch gestures."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    # ---------------------------------------------------------
    # Core Element Interactions & Explicit Waits
    # ---------------------------------------------------------

    def find_element(self, locator: Locator, timeout: float = 10.0) -> WebElement:
        """Find an element on the screen waiting until it is present."""
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator),
            message=f"Element with locator {locator} was not found within {timeout}s",
        )

    def find_elements(self, locator: Locator, timeout: float = 10.0) -> list[WebElement]:
        """Find all elements matching locator waiting until at least one is present."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located(locator),
                message=f"Elements with locator {locator} were not found within {timeout}s",
            )
        except TimeoutException:
            return []

    def click(self, locator: Locator, timeout: float = 10.0) -> None:
        """Wait until element is clickable and perform click."""
        element = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator),
            message=f"Element {locator} was not clickable within {timeout}s",
        )
        element.click()

    def send_keys(
        self,
        locator: Locator,
        text: str,
        clear: bool = True,
        timeout: float = 10.0,
    ) -> None:
        """Wait for element visibility, optionally clear existing content, and type text."""
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator),
            message=f"Element {locator} not visible for text entry within {timeout}s",
        )
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator, timeout: float = 10.0) -> str:
        """Retrieve visible text or content-desc attribute from an element."""
        element = self.find_element(locator, timeout=timeout)
        text = element.text
        if not text:
            # Fallback to Android content-desc or accessibility label
            text = element.get_attribute("content-desc") or element.get_attribute("text") or ""
        return text

    def is_displayed(self, locator: Locator, timeout: float = 5.0) -> bool:
        """Check if an element is visible on screen without raising an uncaught exception."""
        try:
            return bool(
                WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
            )
        except (TimeoutException, NoSuchElementException):
            return False

    # ---------------------------------------------------------
    # Dynamic W3C Gestures (Screen Percentage Calculations)
    # ---------------------------------------------------------

    def swipe(
        self,
        start_x_pct: float,
        start_y_pct: float,
        end_x_pct: float,
        end_y_pct: float,
        duration_ms: int = 800,
    ) -> None:
        """Execute a swipe gesture between dynamic screen percentages via W3C ActionChains."""
        window_size = self.driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        start_x = int(width * start_x_pct)
        start_y = int(height * start_y_pct)
        end_x = int(width * end_x_pct)
        end_y = int(height * end_y_pct)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000.0)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_up(self, duration_ms: int = 800) -> None:
        """Scroll down viewport content by swiping from 80% to 20% vertical height."""
        self.swipe(
            start_x_pct=0.5,
            start_y_pct=0.8,
            end_x_pct=0.5,
            end_y_pct=0.2,
            duration_ms=duration_ms,
        )

    def swipe_down(self, duration_ms: int = 800) -> None:
        """Scroll up viewport content by swiping from 20% to 80% vertical height."""
        self.swipe(
            start_x_pct=0.5,
            start_y_pct=0.2,
            end_x_pct=0.5,
            end_y_pct=0.8,
            duration_ms=duration_ms,
        )

    def swipe_left(self, duration_ms: int = 800) -> None:
        """Swipe viewport leftwards from 80% to 20% horizontal width."""
        self.swipe(
            start_x_pct=0.8,
            start_y_pct=0.5,
            end_x_pct=0.2,
            end_y_pct=0.5,
            duration_ms=duration_ms,
        )

    def swipe_right(self, duration_ms: int = 800) -> None:
        """Swipe viewport rightwards from 20% to 80% horizontal width."""
        self.swipe(
            start_x_pct=0.2,
            start_y_pct=0.5,
            end_x_pct=0.8,
            end_y_pct=0.5,
            duration_ms=duration_ms,
        )

    def scroll_to_text(self, text: str, max_swipes: int = 5) -> WebElement:
        """Scroll dynamically to locate an element containing text.

        First attempts native Android UiScrollable if applicable, then falls back to swipe loop.
        """
        # Attempt Android native UiScrollable
        try:
            ui_scrollable_query = (
                "new UiScrollable(new UiSelector().scrollable(true))"
                f'.scrollIntoView(new UiSelector().textContains("{text}"))'
            )
            return self.find_element(
                (AppiumBy.ANDROID_UIAUTOMATOR, ui_scrollable_query), timeout=3.0
            )
        except Exception:
            pass

        # Cross-platform fallback loop with dynamic swipes
        for _ in range(max_swipes):
            try:
                element = self.find_element(
                    (AppiumBy.XPATH, f"//*[contains(@text, '{text}')]"),
                    timeout=1.5,
                )
                if element.is_displayed():
                    return element
            except (TimeoutException, NoSuchElementException):
                self.swipe_up()

        raise NoSuchElementException(
            f"Failed to find element with text '{text}' after {max_swipes} dynamic swipes."
        )

    def tap_by_coordinates(self, x_pct: float, y_pct: float) -> None:
        """Tap a screen position calculated from relative screen percentages."""
        window_size = self.driver.get_window_size()
        x = int(window_size["width"] * x_pct)
        y = int(window_size["height"] * y_pct)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def long_press(self, locator: Locator, duration_s: float = 2.0) -> None:
        """Perform a touch-and-hold (long press) gesture on a targeted element."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to(element)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_s)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    # ---------------------------------------------------------
    # Device State & Lifecycle Helpers
    # ---------------------------------------------------------

    def background_app(self, seconds: int = 5) -> None:
        """Send the mobile application to background for specified seconds, then resume."""
        self.driver.background_app(seconds)

    def set_orientation(self, orientation: str) -> None:
        """Set screen orientation (PORTRAIT or LANDSCAPE)."""
        self.driver.orientation = orientation.upper()

    def get_orientation(self) -> str:
        """Get the current screen orientation in upper case."""
        return str(self.driver.orientation).upper()

    def hide_keyboard(self) -> None:
        """Safely hide on-screen soft keyboard if currently open."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def handle_permission_alert(self, allow: bool = True) -> None:
        """Handle OS runtime system permission prompts."""
        try:
            alert = self.driver.switch_to.alert
            if allow:
                alert.accept()
            else:
                alert.dismiss()
        except Exception:
            # Fallback to standard Android system dialog buttons
            deny_xpath = (
                "//*[@resource-id='com.android.permissioncontroller:id/permission_deny_button']"
            )
            permission_xpath = (
                "//*[@resource-id='com.android.permissioncontroller:id/permission_allow_button' "
                "or @resource-id='com.android.packageinstaller:id/permission_allow_button']"
                if allow
                else deny_xpath
            )
            try:
                btn = self.find_element((AppiumBy.XPATH, permission_xpath), timeout=2.0)
                btn.click()
            except (TimeoutException, NoSuchElementException):
                pass
