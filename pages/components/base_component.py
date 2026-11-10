"""Base component class for Component Object Model (COM)."""

from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base


class BaseComponent(Base):
    """Base class for all component objects (COM).

    Components encapsulate reusable parts of a screen (e.g. headers, navigation drawers,
    product cards) scoped to their root WebElement.
    """

    root: WebElement  # Type narrowing for mypy: root cannot be None in components

    def __init__(self, root: WebElement) -> None:
        """Initialize the component with its root WebElement."""
        super().__init__(root)

    def is_visible(self) -> bool:
        """Check if component root element is currently displayed on screen."""
        try:
            return bool(self.root.is_displayed())
        except Exception:
            return False
