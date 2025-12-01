# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read environment variable or fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite requires special arguments
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# THIS FUNCTION IS REQUIRED BY FASTAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
