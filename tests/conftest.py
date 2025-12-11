import subprocess
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_server():
    """Start FastAPI server before running Playwright tests."""
    proc = subprocess.Popen(["uvicorn", "app.main:app", "--port", "8000"])
    time.sleep(1.5)  # wait for server to start
    yield
    proc.terminate()
