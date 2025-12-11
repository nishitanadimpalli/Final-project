# tests/test_calculation_integration.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# -------------------------------------------------------------------
# TEST DATABASE (SQLite)
# -------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db_calculations.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# -------------------------------------------------------------------
# OVERRIDE get_db FOR TESTING
# -------------------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -------------------------------------------------------------------
# RESET TABLES BEFORE *EVERY TEST*  (IMPORTANT FIX)
# -------------------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_database():
    """Ensure a clean DB before every test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# -------------------------------------------------------------------
# Helper: REGISTER + LOGIN
# -------------------------------------------------------------------
def register_and_login():
    """Register a user and login using EMAIL + PASSWORD."""
    
    # Register
    client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    # Correct login payload (your auth.py expects email + password)
    response = client.post(
        "/auth/login",
        json={   # <-- JSON is correct (NOT form-data!)
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]


# -------------------------------------------------------------------
# TEST 1 — Create → Read Calculation
# -------------------------------------------------------------------
def test_create_and_read_calculation():
    token = register_and_login()
    headers = {"Authorization": f"Bearer {token}"}

    # Create a calculation
    create_res = client.post(
        "/calculations/",
        json={"a": 5, "b": 3, "type": "Add"},
        headers=headers,
    )

    assert create_res.status_code == 201
    calc_id = create_res.json()["id"]

    # Read calculation
    read_res = client.get(f"/calculations/{calc_id}", headers=headers)
    assert read_res.status_code == 200

    data = read_res.json()
    assert data["a"] == 5
    assert data["b"] == 3
    assert data["result"] == 8


# -------------------------------------------------------------------
# TEST 2 — Stats Endpoint
# -------------------------------------------------------------------
def test_stats_endpoint():
    token = register_and_login()
    headers = {"Authorization": f"Bearer {token}"}

    # Create calculations
    client.post("/calculations/", json={"a": 1, "b": 2, "type": "Add"}, headers=headers)
    client.post("/calculations/", json={"a": 3, "b": 4, "type": "Add"}, headers=headers)
    client.post("/calculations/", json={"a": 10, "b": 5, "type": "Sub"}, headers=headers)

    # Call stats
    res = client.get("/calculations/stats", headers=headers)
    assert res.status_code == 200

    data = res.json()

    # Stats MUST be exactly correct (no extra rows)
    assert data["total_calculations"] == 3
    assert data["add_count"] == 2
    assert data["sub_count"] == 1
    assert data["multiply_count"] == 0
    assert data["divide_count"] == 0
    assert data["avg_a"] == (1 + 3 + 10) / 3
    assert data["avg_b"] == (2 + 4 + 5) / 3
