# CLAUDE.md - Mobile ATQC Bootcamp

## Project Purpose
Bootcamp and hands-on laboratory for Senior Mobile QA Automation Engineers preparing for technical interviews and production-grade automation projects.
Core stack: **Python 3.10+**, **Appium 2.x**, **UiAutomator2**, **XCUITest**, **pytest**, **Pydantic v2**, and **Allure**.
Target demo application: Sauce Labs Demo App (`com.saucelabs.mydemoapp.android`).

---

## Test Execution Commands

```bash
# Run all tests
pytest

# Run critical smoke tests
pytest -m smoke

# Run mobile UI Appium tests
pytest -m mobile

# Run API integration and contract tests
pytest -m api

# Run with environment profiles
pytest --env=local_android
pytest --env=browserstack
pytest --env=local_ios

# Generate Allure reporting results
pytest --alluredir=allure-results

# Combined smoke test run with Allure on local Android
pytest -m smoke --env=local_android --alluredir=allure-results
```

---

## Code Formatting & Linting Commands

```bash
# Check code style, syntax, and imports with Ruff
ruff check .

# Automatically fix autofixable Ruff lint violations
ruff check --fix .

# Format all code according to project style standards
ruff format .

# Strict type checking across all files with mypy
mypy .
```

---

## Architectural & Engineering Rules

### 1. Locator Strategy & Priority
Always adhere to the strict selector hierarchy:
1. **`AppiumBy.ACCESSIBILITY_ID`** (`content-desc` on Android, `accessibilityIdentifier` / `label` on iOS) - Most stable, resilient against UI refactoring, accessibility-friendly.
2. **`AppiumBy.ID`** (`resource-id` on Android) - Stable within package boundaries.
3. **`AppiumBy.ANDROID_UIAUTOMATOR`** / **`AppiumBy.IOS_PREDICATE`** - Fast native platform queries.
4. **`AppiumBy.XPATH`** (Relative only!) - Use only when semantic attributes are missing.
   - **STRICT PROHIBITION**: Never use absolute hierarchy paths such as `/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/...`. Any PR or commit with absolute XPaths will be rejected.

### 2. Page Object Model (POM) & Component Object Model (COM) Architecture
- **Unified Base (`pages/base.py`)**: Foundational class accepting either `WebDriver` (screens) or `WebElement` (scoped components). Automatically scopes XPath queries with `.` prefix when searching inside components.
- **Full Type Annotations (`pages/types.py`)**: `Locator: TypeAlias = tuple[str, str]` and strict return types across every file; fully passes `mypy --strict`.
- **Component Object Model (`pages/components/`)**:
  - `BaseComponent(Base)`: Dedicated component abstraction with type-narrowed `root: WebElement`.
  - `HeaderComponent`: Top navigation bar (title, cart badge, menu button, sort button).
  - `DrawerMenuComponent`: Slide navigation drawer (login/logout, menu items).
  - `ProductCardComponent`: Scoped individual product card in the catalog grid.
- **Modal Dialog Model (`pages/modals/`)**:
  - `BaseModal(Base)`: System and app popups / dialogs (title, message, confirm, cancel).
  - `ConfirmationModal`: Specific confirmation dialogs (e.g. logout confirmation).
- **Strict Separation**: Locators reside in upper-case class attributes at the top of the Page/Component Object. Action methods encapsulate interactions.
- **Fluent Chaining**: Page action methods MUST return `Self` (or target destination Page Object instance) to support clean method chaining in test scenarios.
- **Strict Typing**: Type hints are mandatory on all method arguments and return values (`Self`, `WebElement`, `str`, `int`, `bool`).
- **Assertion Discipline**: No assertions inside Page Object action methods! Assertions belong in tests or dedicated query check methods (e.g. `is_loaded() -> bool`, `get_cart_item_count() -> int`).

### 3. Explicit Waits Only
- **Zero Tolerance for `time.sleep()`**: Hardcoded sleeps are flaky, slow down test suites, and are banned in production code.
- **Dynamic Waiting**: Use `WebDriverWait(driver, timeout).until(...)` with informative custom failure messages.
- Always wait for element visibility, clickability, or staleness depending on the interaction lifecycle.

### 4. Dynamic Gesture Calculation
- **Zero Hardcoded Coordinates**: Coordinates for gestures (`swipe`, `scroll`, `tap`) MUST NEVER be hardcoded pixel values (e.g., `(300, 850)`).
- **Percentage-Based Geometry**: All coordinates must be dynamically computed as ratios/percentages of actual screen dimensions obtained via `driver.get_window_size()`.
- Gestures must use W3C Actions (`ActionChains` / W3C pointer actions) to ensure cross-platform consistency and compatibility with Appium 2.x.

### 5. Device State & Teardown Hygiene
- **App State Isolation**: Each test must start from a predictable, clean state (`no_reset=False` or explicit cache reset).
- **Background/Foreground Resilience**: Verify that apps recover state when placed in the background and resumed.
- **Fail-Safe Driver Teardown**: Drivers must always be quit in fixture teardown (`try ... finally driver.quit()`).
- **Artifact Diagnostics**: Automatic capture of screenshots, logcat, and XML page source dumps upon failure to allow immediate root-cause analysis.

---

## Tooling Recommendations & When to Use

Choose the right tool for the specific stage of the mobile automation lifecycle:

| Tool | Primary Use Case | When to Use | Key Tips & Caveats |
|---|---|---|---|
| **Appium MCP (`appium-mcp`)** | AI-Assisted Development & Inspection | Rapid element discovery, generating Page Objects/locators from live screen, taking screenshots, interactive step debugging. | Attach to active sessions or create local ones; use `generate_locators` to avoid manually typing selector tuples. |
| **Appium Inspector (Desktop)** | Visual Manual Exploration | Deep manual tree inspection, measuring element bounds, recording interaction flows, verifying visual hierarchy. | **Always use Desktop App** (not browser web version to avoid HTTPS/CORS issues). Ensure **"Use SSL" is unchecked**; Remote Path is `/`. |
| **Android Debug Bridge (`adb`)** | Device & OS-Level Control | Device lifecycle (`adb devices`), installing APKs (`adb install -r`), finding active activities (`dumpsys`), clearing cache (`pm clear`), checking native crash logs (`logcat`). | Use `adb shell dumpsys window \| grep -E 'mCurrentFocus'` to find active `appPackage` and `appActivity`. |
| **Pytest Runner** | Automated Suite Execution | Regression, smoke runs (`-m smoke`), environment matrix (`--env=local_android / browserstack / local_ios`), CI execution. | Run with `--alluredir=allure-results` for rich reporting and diagnostic attachments. |
| **Ruff & Mypy** | Code Quality & Type Safety | Pre-commit validation, automated formatting, verifying strict type annotations on Page Objects and tests. | Run `ruff check --fix .`, `ruff format .`, and `mypy .` before committing any code changes. |
| **Allure Report** | Execution Analytics & Triage | Reviewing test results, failure triage, inspecting automatic screenshots, and XML hierarchy dumps. | Generate report via `allure serve allure-results` after test runs. |

### Tool Selection Workflow

```
[Start Task / Screen]
       │
       ├──► Need to inspect UI & write Page Objects?
       │      ├─► Use Appium MCP (`generate_locators`, `appium_screenshot`) for fast AI extraction.
       │      └─► Use Appium Inspector Desktop for complex visual layout or coordinate analysis.
       │
       ├──► Need to diagnose app startup / crashes / package issues?
       │      └─► Use `adb` commands (`adb devices`, `adb logcat`, `pm clear`).
       │
       ├──► Ready to write & verify automated code?
       │      ├─► Write Page Objects following POM/COM in `pages/`.
       │      ├─► Run `mypy .` & `ruff check --fix .` to ensure typing & style compliance.
       │      └─► Execute with `pytest -m <marker> --env=local_android`.
       │
       └──► Test completed or failed?
              └─► Review results and artifacts in `allure-results` / Allure Report.
```
