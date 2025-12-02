Module 13 – FastAPI JWT Authentication + Frontend + CI/CD

This project implements a full-stack FastAPI application with JWT authentication, HTML frontend pages, secure password hashing, database integration, and Playwright end-to-end testing.
GitHub Actions automatically runs all tests, including database integration tests using a PostgreSQL service.

🚀 Features
🔐 Authentication (JWT)

User Registration

Login with email & password

JWT access token generation

Secure password hashing with Passlib (bcrypt)

Token-based protection for backend routes

🖥️ Frontend Pages

/register-page HTML form

/login-page HTML form

Forms call backend using JS fetch()

Alerts on success, failure, or invalid inputs

🧮 API Endpoints

Register user

Login user

Protected calculation routes (CRUD)

Input validation using Pydantic schemas

🗄 Database

PostgreSQL (local + GitHub Actions)

SQLAlchemy ORM

Integration tests create tables automatically

🧪 Testing (Unit + Integration + Playwright)

Unit tests for arithmetic

Schema validation tests

Password hashing tests

Database integration tests

Playwright browser E2E tests for:

Register

Login

⚙️ CI/CD (GitHub Actions)

Runs pytest

Launches a PostgreSQL test container

Installs browsers for Playwright

Fails pipeline if any test fails

▶️ Run the App Locally

Install dependencies:

pip install -r requirements.txt


Start the backend:

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/register-page
http://127.0.0.1:8000/login-page

🧪 Run Tests
pytest -v


For Playwright:

playwright install

📁 Project Structure
app/
 ├── main.py
 ├── models.py
 ├── database.py
 ├── security.py
 ├── schemas.py
 └── routers/
       ├── auth.py
       ├── users.py
       └── calculations.py
public/
 ├── register.html
 └── login.html
tests/
.github/workflows/ci.yml
