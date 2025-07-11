# 🧑‍💼 HR Employee Search System – FastAPI + PostgreSQL

A high-performance, filterable employee directory API for HR organizations, built with FastAPI, PostgreSQL, Alembic, and Docker.

---

## 🚀 Features

- 🔎 Search employees with filters (name, department, position, etc.)
- 🧩 Organization-specific column visibility
- 📄 Pagination support
- 🛡️ Rate limiting middleware
- 🧬 Alembic migrations
- 🌱 Seeder support for test/demo data
- 🐳 Docker & Docker Compose ready

---

## 📁 Project Structure


---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/hr_db



🛠️ Local Development (without Docker)
1. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2. Create DB & run migrations
Make sure PostgreSQL is running locally:
alembic upgrade head


3. Seed sample data
python app/seed_data.py


4. Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



🐳 Run with Docker
1. Build and start services
docker compose up --build

This will:

Start PostgreSQL
Run Alembic migrations
Seed sample data
Launch FastAPI app on http://localhost:8000




🔌 API Endpoints
✅ Health Check
GET /health


✅ Search Employees
GET /api/employees/search


| Param            | Type   | Description                                   |
| ---------------- | ------ | --------------------------------------------- |
| organization\_id | int    | (Required) Organization ID                    |
| name             | string | (Optional) Partial match on name              |
| department       | string | (Optional) Exact department                   |
| position         | string | (Optional) Exact position                     |
| location         | string | (Optional) Exact location                     |
| status           | enum   | (Optional) ACTIVE / NOT\_STARTED / TERMINATED |
| page             | int    | Page number (default: 1)                      |
| page\_size       | int    | Items per page (default: 10)                  |




⚡ Rate Limiting
Configured per IP using middleware

Default: 100 requests per hour

Modify logic in app/main.py or custom middleware



🧑‍💻 Author
Vishal Nitavne
Backend Developer • Python | FastAPI | PostgreSQL
