FastAPI Secure Calculator – Final Project

This project is a full-stack FastAPI web application implementing:

Secure user authentication (JWT)

BREAD operations for calculations

A new feature: User Calculation Statistics

SQLite for local testing + PostgreSQL for production

Full test suite:
✔ Unit Tests
✔ Integration Tests
✔ End-to-End Tests (Playwright)

Dockerized application

Automated CI/CD pipeline with GitHub Actions pushing to Docker Hub

🚀 New Feature: Calculation Statistics

The new feature adds a /calculations/stats backend route and a new stats-page front-end page where the user can:

View total calculations performed

See counts of Add, Sub, Multiply, Divide

View average values of operands A and B

View the results in real time with a “Load My Stats” button

This required:

New backend logic in services/stats.py

New route in routes/calculations.py

New front-end page (stats.html)

New E2E Playwright test validating full workflow

📁 Project Structure
app/
 ├── main.py
 ├── models.py
 ├── database.py
 ├── security.py
 ├── schemas.py
 ├── services/
 │     ├── calculation_factory.py
 │     ├── stats.py
 ├── routes/
 │     ├── users.py
 │     ├── auth.py
 │     ├── calculations.py
 ├── templates/
 │     ├── register.html
 │     ├── login.html
 │     ├── calculations.html
 │     ├── stats.html
tests/
 ├── test_calculation_unit.py
 ├── test_stats_unit.py
 ├── test_calculation_integration.py
 ├── test_e2e.py
requirements.txt
Dockerfile
.github/workflows/ci.yml
README.md

⚙️ How to Run the Application Locally
1️⃣ Create Virtual Environment
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

2️⃣ Install Requirements
pip install -r requirements.txt
playwright install

3️⃣ Run the FastAPI Server
uvicorn app.main:app --reload


Visit:

Register: http://127.0.0.1:8000/register-page

Login: http://127.0.0.1:8000/login-page

Calculations: http://127.0.0.1:8000/calculations-page

Stats Page: http://127.0.0.1:8000/stats-page

🧪 Running Tests
Run All Tests
pytest -q

Run Only E2E Tests
pytest tests/test_e2e.py -q

🐳 Running with Docker
Build Image
docker build -t yourusername/final-project-app .

Run Container
docker run -p 8000:8000 yourusername/final-project-app

🔄 CI/CD Pipeline

This project includes GitHub Actions that automatically:

Install dependencies

Spin up PostgreSQL service

Run all tests (unit + integration + playwright E2E)

Build Docker image

Push image to Docker Hub

The workflow file is located at:

.github/workflows/ci.yml