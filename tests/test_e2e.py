from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_stats_page(page: Page):
    # -------------------------------------------------
    # 1) REGISTER — wait for success message
    # -------------------------------------------------
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", "testuser")
    page.fill("#email", "test@example.com")
    page.fill("#password", "pass123")
    page.fill("#confirm", "pass123")

    page.get_by_role("button", name="Register").click()

    # Wait for backend to confirm
    page.wait_for_timeout(700)

    # Registration should redirect or show message
    # We tolerate duplicate user (CI re-run)
    try:
        expect(page.get_by_text("Registration successful")).to_be_visible(timeout=1200)
    except:
        # If user already exists, continue anyway
        pass

    # -------------------------------------------------
    # 2) LOGIN — must succeed
    # -------------------------------------------------
    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", "test@example.com")
    page.fill("#password", "pass123")

    page.get_by_role("button", name="Login").click()

    page.wait_for_timeout(700)

    # Ensure login was successful by checking token in browser storage
    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None, "❌ Login failed in E2E test — no token stored!"

    # -------------------------------------------------
    # 3) Create calculation
    # -------------------------------------------------
    page.goto(f"{BASE_URL}/calculations-page")
    page.wait_for_timeout(500)

    page.fill("#a", "4")
    page.fill("#b", "2")
    page.select_option("#type", "Divide")
    page.click("#createBtn")

    page.wait_for_timeout(500)

    # -------------------------------------------------
    # 4) Load Stats
    # -------------------------------------------------
    page.goto(f"{BASE_URL}/stats-page")
    page.wait_for_timeout(500)

    page.click("#loadBtn")

    # -------------------------------------------------
    # EXPECT SUCCESS
    # -------------------------------------------------
    expect(page.get_by_text("Stats loaded successfully!")).to_be_visible(timeout=3000)
