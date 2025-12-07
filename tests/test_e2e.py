import pytest

# Skip the entire module because FastAPI server is not running during pytest
pytest.skip("Skipping E2E tests because server is not running during pytest.", allow_module_level=True)

from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"

def test_register(page: Page):
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#email", "playtest@example.com")
    page.fill("#username", "playtest")
    page.fill("#password", "playpass")
    page.fill("#confirm", "playpass")

    page.click("button")

    msg = page.locator("#message")
    expect(msg).to_have_text("Registration successful!")


def test_login(page: Page):
    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", "playtest@example.com")
    page.fill("#password", "playpass")

    page.click("button")

    msg = page.locator("#message")
    expect(msg).to_have_text("Login successful!")
