Module 14 – Secure FastAPI Application with User Auth, CRUD, CI/CD & Docker Deployment

This project implements a secure FastAPI web application with the following features:

🔐 User Registration & Login (JWT-authentication)

➕ Calculator Operations (Add/Sub/Mul/Div)

🔄 Full BREAD CRUD Operations tied to each authenticated user

🧪 Automated Unit, Integration, and Playwright E2E Tests

🐳 Dockerized Application with CI/CD

🚀 GitHub Actions for Testing + Docker Hub Deployment

🗄️ PostgreSQL Database Integration

This repository is the final submission for Module 14, showcasing a complete secure production-ready backend project.

🏗️ Project Structure
app/
│── main.py
│── models.py
│── schemas.py
│── security.py
│── database.py
│── crud_calculations.py
│── crud_users.py
│── routers/
│     ├── auth.py
│     ├── calculations.py
│
templates/
│── login.html
│── register.html
│── calculations.html
│
tests/
│── test_calculation_unit.py
│── test_calculation_integration.py
│── test_users_integration.py
│── test_schemas.py
│── test_security.py
│── test_e2e.py
│
Dockerfile
requirements.txt

🔐 Features Overview
✔ 1. User Authentication

Register with unique username + email

Passwords are hashed using Passlib (bcrypt)

Log in to receive a JWT access token

All authenticated routes require valid JWT

✔ 2. Calculations (CRUD/BREAD)

Each user can:

Create a calculation

Read a single calculation

Edit their own calculation

Delete their calculation

Browse all calculations belonging to them

Supported operations:

Add, Subtract, Multiply, Divide

✔ 3. Database

Uses PostgreSQL with SQLAlchemy ORM.

Environment variable:

DATABASE_URL=postgresql://calcuser:calcpass@localhost:5432/module10db

Run all tests:
pytest -vv

🐳 Docker Support

The project ships with a production-ready Dockerfile.

Build manually:
docker build -t yourname/module14 .

Run:
docker run -p 8000:8000 yourname/module14

🚀 CI/CD Using GitHub Actions

Two workflows automate this project:

1️⃣ ci.yml — Test Pipeline

Runs on every commit:

Sets up PostgreSQL service

Installs dependencies

Runs FastAPI server

Executes all tests

2️⃣ docker-publish.yml — Deployment Pipeline

On every push to main, this workflow:

Builds Docker image

Logs in to Docker Hub

Pushes:

yourname/module14:latest

yourname/module14:<commit-sha>

Secrets required:

DOCKER_USERNAME
DOCKER_TOKEN

▶️ Running the App Locally
1. Install dependencies
pip install -r requirements.txt

2. Start server
uvicorn app.main:app --reload

3. Open in browser:
http://127.0.0.1:8000/register-page