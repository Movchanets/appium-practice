"""Pytest configuration and fixture management for Mobile ATQC Bootcamp."""

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

try:
    import allure
except ImportError:
    allure = None


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom command-line options for test execution."""
    parser.addoption(
        "--env",
        action="store",
        default="local_android",
        choices=["local_android", "local_ios", "browserstack"],
        help="Target execution environment: local_android, local_ios, or browserstack",
    )
    parser.addoption(
        "--app-path",
        action="store",
        default=None,
        help="Path to the mobile application binary (.apk or .ipa)",
    )
    parser.addoption(
        "--device-name",
        action="store",
        default=None,
        help="Target device name or emulator ID (e.g. Pixel_7_API_34)",
    )
    parser.addoption(
        "--udid",
        action="store",
        default=os.getenv("ANDROID_SERIAL", None),
        help="Unique Device Identifier (UDID) for targeting a specific device",
    )


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
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.app_package = "com.saucelabs.mydemoapp.android"
        options.app_activity = "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
        options.app_wait_activity = "com.saucelabs.mydemoapp.android.view.activities.*"
        options.no_reset = True
        options.auto_grant_permissions = True
        options.new_command_timeout = 300
        if app_path:
            options.app = app_path
        if device_name:
            options.device_name = device_name
        if udid:
            options.udid = udid

        active_driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            options=options,
        )

    elif env == "local_ios":
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.automation_name = "XCUITest"
        options.no_reset = False
        options.new_command_timeout = 300
        if app_path:
            options.app = app_path
        if device_name:
            options.device_name = device_name

        active_driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            options=options,
        )

    elif env == "browserstack":
        bs_username = os.getenv("BROWSERSTACK_USERNAME", "demo_user")
        bs_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY", "demo_key")
        bs_app_id = os.getenv("BROWSERSTACK_APP_ID", "bs://sampleAppId")

        options = UiAutomator2Options()
        bstack_options = {
            "userName": bs_username,
            "accessKey": bs_access_key,
            "app": bs_app_id,
            "projectName": "Mobile ATQC Bootcamp",
            "buildName": "SauceDemo Android Build",
            "sessionName": request.node.name,
        }
        options.set_capability("bstack:options", bstack_options)
        options.set_capability("platformName", "android")
        options.set_capability("appium:automationName", "UiAutomator2")

        active_driver = webdriver.Remote(
            command_executor="http://hub-cloud.browserstack.com/wd/hub",
            options=options,
        )
    else:
        raise ValueError(f"Unsupported environment configuration: {env}")

    # Attach driver reference to request node for failure diagnostics hook
    request.node.driver = active_driver

    try:
        yield active_driver
    finally:
        active_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: Any) -> Generator[None, Any, None]:
    """Hook executed upon test phase completion.

    On failure during test call, captures screenshot, page source XML, and Android logcat.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        active_driver = getattr(item, "driver", None)
        if active_driver is None:
            return

        test_name = item.name.replace("/", "_").replace("::", "_")

        artifacts_dir = Path("artifacts")
        screenshots_dir = artifacts_dir / "screenshots"
        page_sources_dir = artifacts_dir / "page_sources"
        logs_dir = artifacts_dir / "logs"

        screenshots_dir.mkdir(parents=True, exist_ok=True)
        page_sources_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)

        # 1. Screenshot capture
        try:
            screenshot_path = screenshots_dir / f"{test_name}.png"
            screenshot_bytes = active_driver.get_screenshot_as_png()
            screenshot_path.write_bytes(screenshot_bytes)
            if allure:
                allure.attach(
                    screenshot_bytes,
                    name=f"{test_name}_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception as exc:
            print(f"\n[Artifact Diagnostics] Failed to capture screenshot: {exc}")

        # 2. Page source XML capture
        try:
            page_source = active_driver.page_source
            page_source_path = page_sources_dir / f"{test_name}.xml"
            page_source_path.write_text(page_source, encoding="utf-8")
            if allure:
                allure.attach(
                    page_source,
                    name=f"{test_name}_page_source",
                    attachment_type=allure.attachment_type.XML,
                )
        except Exception as exc:
            print(f"\n[Artifact Diagnostics] Failed to capture page source: {exc}")

        # 3. Android Logcat capture (last 100 entries)
        try:
            logcat_entries = active_driver.get_log("logcat")
            last_entries = logcat_entries[-100:] if len(logcat_entries) > 100 else logcat_entries
            logcat_text = "\n".join(
                f"{entry.get('timestamp', '')} [{entry.get('level', '')}] "
                f"{entry.get('message', '')}"
                for entry in last_entries
            )
            logcat_path = logs_dir / f"{test_name}_logcat.log"
            logcat_path.write_text(logcat_text, encoding="utf-8")
            if allure:
                allure.attach(
                    logcat_text,
                    name=f"{test_name}_logcat",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception:
            # Platform might not support logcat (e.g. iOS or remote cloud limitations)
            pass
