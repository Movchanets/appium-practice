"""Appium WebDriver lifecycle fixtures."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    """Initialize and yield the mobile Appium driver instance per test.

    Ensures proper teardown by safely quitting the driver after test completion.
    """
    env = request.config.getoption("--env")
    app_path = request.config.getoption("--app-path")
    device_name = request.config.getoption("--device-name")
    udid = request.config.getoption("--udid")

    active_driver: webdriver.Remote

    if env == "local_android":
        android_options = UiAutomator2Options()
        android_options.platform_name = "Android"
        android_options.automation_name = "UiAutomator2"
        android_options.app_package = "com.saucelabs.mydemoapp.android"
        android_options.app_activity = (
            "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
        )
        android_options.app_wait_activity = "com.saucelabs.mydemoapp.android.view.activities.*"
        android_options.no_reset = True
        android_options.auto_grant_permissions = True
        android_options.new_command_timeout = 300
        if app_path:
            android_options.app = app_path
        if device_name:
            android_options.device_name = device_name
        if udid:
            android_options.udid = udid

        active_driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            options=android_options,
        )

    elif env == "local_ios":
        ios_options = XCUITestOptions()
        ios_options.platform_name = "iOS"
        ios_options.automation_name = "XCUITest"
        ios_options.no_reset = False
        ios_options.new_command_timeout = 300
        if app_path:
            ios_options.app = app_path
        if device_name:
            ios_options.device_name = device_name

        active_driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            options=ios_options,
        )

    elif env == "browserstack":
        bs_username = os.getenv("BROWSERSTACK_USERNAME", "demo_user")
        bs_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY", "demo_key")
        bs_app_id = os.getenv("BROWSERSTACK_APP_ID", "bs://sampleAppId")

        bs_options = UiAutomator2Options()
        bstack_options = {
            "userName": bs_username,
            "accessKey": bs_access_key,
            "app": bs_app_id,
            "projectName": "Mobile ATQC Bootcamp",
            "buildName": "SauceDemo Android Build",
            "sessionName": request.node.name,
        }
        bs_options.set_capability("bstack:options", bstack_options)
        bs_options.set_capability("platformName", "android")
        bs_options.set_capability("appium:automationName", "UiAutomator2")

        active_driver = webdriver.Remote(
            command_executor="http://hub-cloud.browserstack.com/wd/hub",
            options=bs_options,
        )
    else:
        raise ValueError(f"Unsupported environment configuration: {env}")

    # Attach driver reference to request node for failure diagnostics hook
    request.node.driver = active_driver

    try:
        yield active_driver
    finally:
        active_driver.quit()
