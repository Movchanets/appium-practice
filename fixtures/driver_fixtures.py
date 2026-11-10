"""Appium WebDriver lifecycle fixtures."""

from __future__ import annotations

import contextlib
import os
import tempfile
import time
from collections.abc import Generator
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")


@contextlib.contextmanager
def _device_session_lock(device_id: str, timeout_s: float = 600.0) -> Generator[None, None, None]:
    """Cross-process file lock to prevent parallel pytest workers from colliding on one emulator."""
    raw_id = device_id or "default"
    safe_id = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in raw_id)
    lock_path = Path(tempfile.gettempdir()) / f"appium_device_lock_{safe_id}.lock"
    deadline = time.monotonic() + timeout_s
    fd: int | None = None

    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, f"{os.getpid()}".encode())
            break
        except FileExistsError:
            # Remove stale lock if holder PID is no longer alive
            with contextlib.suppress(OSError, ValueError):
                raw_pid = lock_path.read_text(encoding="utf-8").strip()
                if raw_pid:
                    pid = int(raw_pid)
                    try:
                        os.kill(pid, 0)
                    except OSError:
                        lock_path.unlink(missing_ok=True)
                        continue
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Timed out waiting for exclusive device lock: {lock_path}"
                ) from None
            time.sleep(0.5)

    try:
        yield
    finally:
        if fd is not None:
            with contextlib.suppress(OSError):
                os.close(fd)
        with contextlib.suppress(OSError):
            lock_path.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    """Initialize and yield the mobile Appium driver instance per test.

    Acquires a cross-process file lock per target device/UDID so concurrent processes
    never collide on the same emulator, and ensures proper teardown via driver.quit().
    """
    env = request.config.getoption("--env")
    app_path = request.config.getoption("--app-path")
    device_name = request.config.getoption("--device-name")
    udid = request.config.getoption("--udid")
    appium_url: str = request.config.getoption("--appium-url") or APPIUM_SERVER_URL
    platform_version = request.config.getoption("--platform-version")

    lock_key = str(udid or device_name or env or "default")
    with _device_session_lock(lock_key):
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
            android_options.no_reset = False
            android_options.auto_grant_permissions = True
            android_options.new_command_timeout = 300
            if app_path:
                android_options.app = app_path
            if device_name:
                android_options.device_name = device_name
            if udid:
                android_options.udid = udid
            if platform_version:
                android_options.platform_version = str(platform_version)

            active_driver = webdriver.Remote(
                command_executor=appium_url,
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
            if platform_version:
                ios_options.platform_version = str(platform_version)

            active_driver = webdriver.Remote(
                command_executor=appium_url,
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
            if platform_version:
                bstack_options["osVersion"] = str(platform_version)
            bs_options.set_capability("bstack:options", bstack_options)
            bs_options.set_capability("platformName", "android")
            bs_options.set_capability("appium:automationName", "UiAutomator2")

            active_driver = webdriver.Remote(
                command_executor="https://hub-cloud.browserstack.com/wd/hub",
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
