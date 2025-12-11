from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_stats_page(page: Page):
    # --------------------------
    # 1) REGISTER
    # --------------------------
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", "testuser")
    page.fill("#email", "test@example.com")
    page.fill("#password", "pass123")
    page.fill("#confirm", "pass123")

    page.get_by_role("button", name="Register").click()

    # --------------------------
    # 2) LOGIN
    # --------------------------
    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", "test@example.com")
    page.fill("#password", "pass123")

    page.get_by_role("button", name="Login").click()

    # ⭐ WAIT so JS stores token in localStorage
    page.wait_for_timeout(700)

    # --------------------------
    # 3) Create a calculation
    # --------------------------
    page.goto(f"{BASE_URL}/calculations-page")

    # ⭐ WAIT for page JS to finish auto-loading
    page.wait_for_timeout(500)

    page.fill("#a", "4")
    page.fill("#b", "2")
    page.select_option("#type", "Divide")

    page.click("#createBtn")

    # --------------------------
    # 4) Load Stats
    # --------------------------
    page.goto(f"{BASE_URL}/stats-page")

    page.wait_for_timeout(500)

    page.click("#loadBtn")

    # --------------------------
    # EXPECT SUCCESS
    # --------------------------
    expect(page.get_by_text("Stats loaded successfully!")).to_be_visible()
