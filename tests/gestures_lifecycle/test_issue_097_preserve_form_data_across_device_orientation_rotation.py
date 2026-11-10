"""TC-097: Preserve Form Data Across Device Orientation Rotation."""

from __future__ import annotations

import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.mobile
@pytest.mark.practice
@allure.feature("Login Screen")
@allure.story("Device Rotation")
@allure.title("Preserve form data across device orientation rotation")
@allure.issue("97")
@pytest.mark.xfail(
    reason=(
        "BUG: App is hardcoded to portrait mode in AndroidManifest.xml (Orientation change ignored)"
    ),
    strict=False,
)
def test_preserve_form_data_across_device_orientation_rotation(login_page: LoginPage) -> None:
    """

    Preconditions:
        User is on Login screen and enters 'tactical_operator' in Username field.
    Steps:
        1. Rotate device orientation to Landscape.
        2. Check the Username field.
        3. Rotate device orientation back to Portrait.
        4. Check the device orientation.
        5. Check the Username field.
    """
    with allure.step("Precondition: User is on Login screen and enters 'tactical_operator'"):
        login_page.enter_username("tactical_operator")

    with allure.step("Step 1: Rotate device orientation to Landscape"):
        initial_orientation = login_page.get_orientation()
        login_page.rotate_to_landscape()
        assert login_page.get_orientation() != initial_orientation, (
            "Orientation did not change to Landscape"
        )

    with allure.step("Step 2: Check the Username field in Landscape"):
        assert login_page.get_username() == "tactical_operator", (
            "Username reset after rotating to Landscape"
        )

    with allure.step("Step 3: Rotate device orientation back to Portrait"):
        landscape_orientation = login_page.get_orientation()
        login_page.rotate_to_portrait()
        assert login_page.get_orientation() != landscape_orientation, (
            "Orientation did not change back to Portrait"
        )

    with allure.step("Step 4: Check that device orientation is Portrait"):
        assert login_page.get_orientation() == "PORTRAIT", "Current orientation is not Portrait"

    with allure.step("Step 5: Check the Username field in Portrait"):
        assert login_page.get_username() == "tactical_operator", (
            "Username reset after rotating back to Portrait"
        )
