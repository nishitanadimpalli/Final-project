import os
import pytest

# If PostgreSQL is not running, skip the entire test module
import socket

def postgres_running(host="localhost", port=5432):
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except Exception:
        return False

if not postgres_running():
    pytest.skip("Skipping user integration tests because PostgreSQL is not running.", allow_module_level=True)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models, schemas
from app.crud_users import create_user, get_user_by_username, get_user_by_email
from app.security import verify_password


TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://calcuser:calcpass@localhost:5432/module10db",
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        session.query(models.User).delete()
        session.commit()
        yield session
    finally:
        session.close()


def test_create_user_and_uniqueness(db):
    user_data = schemas.UserCreate(
        username="user1",
        email="user1@example.com",
        password="password123",
    )

    user = create_user(db, user_data)
    assert user.id is not None
    assert user.username == "user1"
    assert user.email == "user1@example.com"
    assert verify_password("password123", user.password_hash)

    from sqlalchemy.exc import IntegrityError

    dup_user = schemas.UserCreate(
        username="user1",
        email="another@example.com",
        password="password456",
    )

    with pytest.raises(IntegrityError):
        create_user(db, dup_user)


def test_get_user_by_username_and_email(db):
    user_data = schemas.UserCreate(
        username="user2",
        email="user2@example.com",
        password="password123",
    )
    create_user(db, user_data)

    u1 = get_user_by_username(db, "user2")
    assert u1 is not None
    assert u1.email == "user2@example.com"

    u2 = get_user_by_email(db, "user2@example.com")
    assert u2 is not None
    assert u2.username == "user2"
