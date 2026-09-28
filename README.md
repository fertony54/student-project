# 🎓 Student Management API with CI/CD Pipeline

A production-structured REST API built with **FastAPI** demonstrating clean architecture, comprehensive testing, and a complete CI/CD pipeline using **GitHub Actions** with automatic deployment to **Render**.

> **Portfolio Project** — Perfect for freshers to showcase backend, testing, and DevOps skills.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Quick Start (Local)](#-quick-start-local)
- [API Reference](#-api-reference)
- [Running Tests](#-running-tests)
- [CI/CD Pipeline Explained](#-cicd-pipeline-explained)
- [Deploying to Render](#-deploying-to-render)
- [Architecture Decisions](#-architecture-decisions)

---

## ✨ Features

| Feature | Details |
|---|---|
| **Full CRUD** | Create, Read, Update (partial), Delete students |
| **Pagination** | Page + page_size query params |
| **Search & Filter** | Search by name/email, filter by department |
| **Statistics** | Aggregate stats: averages, department breakdown |
| **Validation** | Pydantic v2 schemas with custom validators |
| **Error Handling** | Consistent HTTP error codes (404, 409, 422) |
| **Auto Docs** | Swagger UI at `/docs`, ReDoc at `/redoc` |
| **50 Tests** | Unit + integration, 97% code coverage |
| **CI/CD** | 5-stage GitHub Actions pipeline |
| **1-Click Deploy** | Render deployment with health checks |

---

## 🗂 Project Structure

```
student-management-api/
│
├── app/                          # Application source
│   ├── main.py                   # FastAPI app, middleware, routers
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── students.py   # Route handlers (thin layer)
│   ├── core/
│   │   └── config.py             # Settings via pydantic-settings
│   ├── db/
│   │   └── database.py           # SQLAlchemy engine + session
│   ├── models/
│   │   └── student.py            # ORM model (DB table)
│   ├── schemas/
│   │   └── student.py            # Pydantic schemas (request/response)
│   └── services/
│       └── student_service.py    # Business logic + DB operations
│
├── tests/
│   ├── conftest.py               # Shared pytest fixtures
│   ├── unit/
│   │   └── test_schemas.py       # Pydantic validation tests
│   └── integration/
│       └── test_students_api.py  # Full HTTP endpoint tests
│
├── scripts/
│   ├── seed_data.py              # Populate DB with sample students
│   └── run.sh                    # Dev server startup script
│
├── .github/
│   └── workflows/
│       ├── ci-basic.yml          # Minimal starter pipeline (teaching, manual run)
│       └── ci-cd.yml             # Full 5-stage CI/CD pipeline
│
├── Dockerfile                    # Container image for consistent packaging
├── .dockerignore
├── requirements.txt
├── pyproject.toml                # pytest + black + isort config
├── .flake8                       # Linter config
├── render.yaml                   # Render deployment config
├── Procfile                      # Process file for deployment
└── .env.example                  # Environment variable template
```

> **Teaching note:** There are two workflows on purpose. `ci-basic.yml` is the
> *minimal* pipeline from the concept notes (checkout → setup → install → lint →
> test) and runs only when triggered by hand. `ci-cd.yml` is the full pipeline.
> Show the small one first, then graduate to the full one. A companion
> **Instructor Teaching Guide** walks through every concept using this project.

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **FastAPI** | Web framework (async, auto-docs) |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic v2** | Request/response validation |
| **pydantic-settings** | Config from environment variables |
| **SQLite** | Database (local dev; swap for PostgreSQL in prod) |
| **Pytest** | Test runner |
| **pytest-cov** | Code coverage reports |
| **httpx** | Async HTTP client for TestClient |
| **Black** | Code formatter |
| **isort** | Import sorter |
| **Flake8** | Linter |
| **GitHub Actions** | CI/CD automation |
| **Render** | Cloud deployment platform |

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.10+ installed
- Git installed

### 1. Clone and Set Up

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/student-management-api.git
cd student-management-api

# Create and activate virtual environment
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# The defaults work out of the box for local development
# Edit .env if you need to change DATABASE_URL or SECRET_KEY
```

### 4. Run the Server

```bash
# Option A: Using the helper script (recommended)
bash scripts/run.sh

# Option B: With sample data pre-seeded
bash scripts/run.sh --seed

# Option C: Direct uvicorn
uvicorn app.main:app --reload --port 8000
```

### 5. Open in Browser

| URL | Description |
|---|---|
| http://localhost:8000 | Root endpoint |
| http://localhost:8000/docs | **Swagger UI** (interactive) |
| http://localhost:8000/redoc | ReDoc documentation |
| http://localhost:8000/health | Health check |

---

## 📡 API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### ➕ Create Student
```http
POST /api/v1/students/
Content-Type: application/json

{
  "first_name": "Alice",
  "last_name": "Sharma",
  "email": "alice@university.edu",
  "age": 21,
  "grade": 8.5,
  "department": "Computer Science"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "first_name": "Alice",
  "last_name": "Sharma",
  "email": "alice@university.edu",
  "age": 21,
  "grade": 8.5,
  "department": "Computer Science",
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2025-01-01T10:00:00"
}
```

---

#### 📋 List Students (with pagination & search)
```http
GET /api/v1/students/?page=1&page_size=10&department=Computer&search=Alice
```

**Response** `200 OK`
```json
{
  "total": 1,
  "page": 1,
  "page_size": 10,
  "students": [...]
}
```

---

#### 🔍 Get Student by ID
```http
GET /api/v1/students/1
```

---

#### ✏️ Update Student (partial)
```http
PATCH /api/v1/students/1
Content-Type: application/json

{
  "grade": 9.2,
  "department": "Data Science"
}
```
Only the provided fields are updated. All others remain unchanged.

---

#### 🗑️ Delete Student
```http
DELETE /api/v1/students/1
```

---

#### 📊 Get Statistics
```http
GET /api/v1/students/stats
```

**Response** `200 OK`
```json
{
  "total_students": 6,
  "average_grade": 8.23,
  "average_age": 21.8,
  "highest_grade": 9.8,
  "lowest_grade": 6.9,
  "students_per_department": {
    "Computer Science": 2,
    "Mathematics": 1,
    "Data Science": 1
  }
}
```

---

### Validation Rules

| Field | Rule |
|---|---|
| `first_name` / `last_name` | 1–50 chars, letters/hyphens/apostrophes only, auto title-cased |
| `email` | Valid email format, must be unique |
| `age` | Integer between 16 and 100 |
| `grade` | Float between 0.0 and 10.0 |
| `department` | 2–100 characters |

### Error Responses

| Code | Meaning |
|---|---|
| `422 Unprocessable Entity` | Validation failed (bad input) |
| `404 Not Found` | Student ID does not exist |
| `409 Conflict` | Email already registered |

---

## 🧪 Running Tests

```bash
# Run all 50 tests
pytest

# Run with verbose output
pytest -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Run a specific test class
pytest tests/integration/test_students_api.py::TestCreateStudent -v

# Run a specific test
pytest tests/integration/test_students_api.py::TestCreateStudent::test_create_student_success -v
```

### Expected Output
```
50 passed in 1.86s
Coverage: 97%
```

---

## ⚙️ CI/CD Pipeline Explained

The pipeline in `.github/workflows/ci-cd.yml` has **5 stages** that run sequentially:

```
Push to GitHub
      │
      ▼
┌─────────────────┐
│ 1. Code Quality │  black + isort + flake8
└────────┬────────┘
         │ (must pass)
         ▼
┌────────────────────────────────────────┐
│  2. Tests (parallel: Python 3.10/11/12) │  pytest + coverage ≥80%
└────────┬───────────────────────────────┘
         │        │
         │   3. Security Scan  safety + bandit
         │
         ▼ (both must pass)
┌────────────────────┐
│ 4. Build & Smoke   │  import check + /health endpoint
└────────┬───────────┘
         │ (only on push to main)
         ▼
┌────────────────────┐
│ 5. Deploy to Render│  webhook + post-deploy health check
└────────────────────┘
```

### What each job does

**Job 1 — Code Quality**
- `black --check` → enforces consistent formatting
- `isort --check` → enforces sorted imports
- `flake8` → catches syntax errors and style issues

**Job 2 — Tests**
- Runs on Python 3.10, 3.11, and 3.12 in parallel (matrix strategy)
- Fails the pipeline if coverage drops below 80%
- Uploads coverage XML as an artifact

**Job 3 — Security**
- `safety` → checks all packages for known CVEs
- `bandit` → static analysis for common security issues

**Job 4 — Build & Smoke Test**
- Verifies the app can be imported without errors
- Starts the server and hits `/health` — fails if it returns non-200

**Job 5 — Deploy** *(main branch only)*
- Fires a Render Deploy Hook (webhook URL)
- Waits 60 seconds then checks `/health` on the production URL

---

## 🌐 Deploying to Render

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial Student Management API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/student-management-api.git
git push -u origin main
```

### Step 2 — Create a Render Web Service

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Render auto-detects `render.yaml` — review settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`
5. Click **Deploy**

### Step 3 — Get the Deploy Hook URL

1. In Render dashboard → Your Service → **Settings**
2. Scroll to **Deploy Hook** → copy the URL
3. In GitHub → Repository **Settings → Secrets → Actions**
4. Add secret: `RENDER_DEPLOY_HOOK_URL` = (the URL you copied)
5. Add secret: `RENDER_APP_URL` = (your Render URL, e.g. `https://student-api.onrender.com`)

### Step 4 — Trigger the Pipeline

```bash
# Make any change and push to main
git commit --allow-empty -m "ci: trigger deployment"
git push origin main
```

Watch the pipeline at: `https://github.com/YOUR_USERNAME/student-management-api/actions`

---

## 🏗 Architecture Decisions

### Why Layered Architecture?

```
Request → Router (endpoint) → Service (business logic) → Model (database)
Response ← Schema (serialization) ← Service ← Model
```

- **Endpoints** are thin — they only validate input and call the service
- **Services** contain all logic — easy to test without HTTP overhead  
- **Schemas** are separate from models — API contract doesn't leak DB details

### Why SQLite for dev, PostgreSQL for prod?

SQLite requires zero setup and works everywhere. The `DATABASE_URL` env var lets you swap to PostgreSQL on Render with one config change — the SQLAlchemy code is identical.

### Why PATCH instead of PUT for updates?

PATCH allows partial updates (only send changed fields). PUT would require sending the full object every time, which is inconvenient for clients.

### Why fixture-per-test isolation?

Each test creates fresh tables and drops them after. This prevents test pollution — a failing test never affects another test.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Run tests: `pytest`
5. Check formatting: `black app/ tests/ && isort app/ tests/`
6. Push and open a Pull Request

---

## 📄 License

MIT License — free to use for learning and portfolio projects.


