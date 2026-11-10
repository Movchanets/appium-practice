"""Types and type aliases for Page and Component Object Models."""

from typing import Literal, TypeAlias

# Standard locator tuple expected by Selenium & Appium (by, value)
Locator: TypeAlias = tuple[str, str]

# Device orientation types
ScreenOrientation: TypeAlias = Literal["PORTRAIT", "LANDSCAPE"]

# Dynamic gesture directions
SwipeDirection: TypeAlias = Literal["up", "down", "left", "right"]

# Catalog sorting options
SortOption: TypeAlias = Literal["name_asc", "name_desc", "price_asc", "price_desc"]

# Product color variants
ProductColor: TypeAlias = Literal["black", "blue", "gray", "green"]
