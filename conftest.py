"""Pytest configuration, CLI options, failure diagnostics hooks, and fixture plugin registration."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from appium import webdriver

pytest.register_assert_rewrite("fixtures")

pytest_plugins = [
    "fixtures.driver_fixtures",
    "fixtures.page_fixtures",
    "fixtures.component_fixtures",
    "fixtures.modal_fixtures",
]


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: Any) -> Generator[None, Any, None]:
    """Hook executed upon test phase completion.

    On failure during test call, captures screenshot, page source XML, and Android logcat.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        active_driver: webdriver.Remote | None = getattr(item, "driver", None)
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
            if allure is not None:
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
            if allure is not None:
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
            if allure is not None:
                allure.attach(
                    logcat_text,
                    name=f"{test_name}_logcat",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception:
            # Platform might not support logcat (e.g. iOS or remote cloud limitations)
            pass
