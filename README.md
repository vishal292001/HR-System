# 🧑‍💼 HR Employee Search System – FastAPI + PostgreSQL

A high-performance, filterable employee directory API for HR organizations, built with FastAPI, PostgreSQL, Alembic, and Docker.

---

## 🚀 Features

- 🔍 Employee search with flexible filters
- 🏢 Organization-specific visible columns
- 📄 Pagination support
- 🔐 Rate limiting middleware
- ⚙️ Alembic-based migrations
- 🌱 Seeder for development/test data
- 🐳 Docker & Docker Compose support

---

## 📁 Project Structure

```
hr_system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── config.py
│   ├── models.py
│   ├── routers/
│   ├── crud/
│   └── seed.py
├── alembic/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── start.sh
├── .env
└── README.md
```

---

## ⚙️ Environment Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/hr_db
```

---

## 💻 Running Locally (No Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

alembic upgrade head
python app/seed.py

uvicorn app.main:app --reload
```

---

## 🐳 Running with Docker

```bash
docker compose up --build
```

- Runs DB, app, migrations, and seeds data
- Access API at: http://localhost:8000

---

## 🔌 API Endpoints

### Health

```http
GET /health
```

### Employee Search

```http
GET /api/employees/search
```

#### Filters

| Query Param    | Type     | Description                                 |
|----------------|----------|---------------------------------------------|
| organization_id| int      | Required                                     |
| name           | string   | Optional, partial match                      |
| department     | string   | Optional                                     |
| position       | string   | Optional                                     |
| location       | string   | Optional                                     |
| status         | enum     | ACTIVE, NOT_STARTED, TERMINATED             |
| page           | int      | Default = 1                                  |
| page_size      | int      | Default = 10                                 |

Example:

```bash
curl -X GET "http://localhost:8000/api/employees/search?organization_id=1&page=1&page_size=5"
```

---

## 🧬 Alembic Migrations

```bash
alembic revision --autogenerate -m "add something"
alembic upgrade head
```

---

## 🌱 Seeder

```bash
python app/seed.py
```

Runs automatically in Docker via `start.sh`

---

## 🛡️ Rate Limiting

Basic in-memory rate limit included. Can be extended using Redis or other backends.

---

## 🧑‍💻 Author

**Vishal Nitavne**  
Backend Developer | FastAPI | PostgreSQL | Kafka

---
