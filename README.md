# automation-center-f78c-2bKennethWilliams minor text refresh

> **Lightweight Automation Task Center** — FastAPI + SQLAlchemy backend with clean CRUD, search, config-driven UX, and seamless extensibility. minor text refresh.

A minimal, production-ready automation task platform for individual developers. Built for clarity, smooth interaction, and future growth — with explicit hooks for Celery/Redis, CI/CD readiness, and zero boilerplate bloat.

**Scheme Identifier**: `PROMPT-F78CD1-000083`

---

## ✨ Features

- ✅ Full RESTful CRUD for `Task` (id, title, status, created_at, updated_at)
- ✅ Interactive Swagger UI (`/docs`) & ReDoc (`/redoc`) out-of-the-box
- ✅ Local static fake data loader (`core/fake_data.py`) — no DB setup needed to start
- ✅ In-memory fuzzy search (`/api/v1/tasks/search`) — designed to swap in PostgreSQL full-text or Elasticsearch later
- ✅ Config-first design: `.env`-driven settings with sane defaults (`config.py`)
- ✅ Async SQLAlchemy 2.0+ stack with connection pooling & health check (`database.py`)
- ✅ `/settings` endpoint — static configuration surface with extension hooks (e.g., for auth, notifications, integrations)
- ✅ `/health` endpoint with DB connectivity validation
- ✅ Alembic migration scaffold (`alembic/`) — async-ready placeholder (commented for `asyncpg`/`sqlalchemy>=2.0`)
- ✅ Docker + docker-compose for local dev & CI/CD build reproducibility
- ✅ Flat, readable structure — no nested abstractions; all modules purpose-dedicated

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- `pip` (≥23.0 recommended)
- Optional: Docker & docker-compose (for containerized dev)

### Run Locally

```bash
# 1. Clone & enter
$ git clone https://github.com/your/automation-center-f78c-2bKennethWilliams.git
$ cd automation-center-f78c-2bKennethWilliams

# 2. Set up environment
$ cp .env.example .env  # edit DATABASE_URL if using real DB

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Load fake data (optional, for demo)
$ python -c "from core.fake_data import load_sample_tasks; load_sample_tasks()"

# 5. Start server
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Visit `http://localhost:8000/docs` to explore the API interactively.

### Run with Docker

```bash
$ docker-compose up --build
```

Then access:
- App: `http://localhost:8000/docs`  
- Adminer (DB GUI): `http://localhost:8080` (login with `.env` DB credentials)

---

## 🧱 Architecture Overview

```
.
├── main.py                # Lifespan-managed FastAPI app entry
├── config.py              # Env-aware config (DEBUG, DATABASE_URL, SECRET_KEY, etc.)
├── database.py            # Async engine + session dep, health helper
├── models/                # SQLAlchemy ORM models (task.py → Task)
├── schemas/               # Pydantic v2 schemas (Create, Read, Update, SearchQuery)
├── api/
│   ├── __init__.py        # Route aggregation
│   └── v1/
│       ├── __init__.py    # Versioned router mount
│       ├── tasks.py       # CRUD + /search
│       ├── settings.py    # GET /settings — static config surface + extensibility hook
│       └── health.py      # GET /health + DB ping
├── core/
│   ├── fake_data.py       # Pure dict-based sample tasks (no ORM overhead)
│   └── search.py          # Memory-resident fuzzy matcher (title/description)
├── alembic/               # Migration scaffolding (env.py + versions/)
├── alembic.ini            # Async-migration ready config (comments guide next steps)
├── .env                   # Local env vars (gitignored)
└── Dockerfile + docker-compose.yml
```

No hidden layers. No magic. Every file has one clear responsibility.

---

## ⚙️ Environment Dependencies

| Tool             | Purpose                                     |
|------------------|---------------------------------------------|
| `fastapi`        | Web framework (ASGI, OpenAPI-native)        |
| `sqlalchemy>=2.0`| Async ORM + Core (future-proof, no legacy)  |
| `uvicorn`        | Production ASGI server                      |
| `python-dotenv`  | Safe `.env` loading                         |
| `alembic`        | Database migration tooling (scaffolded)       |
| `pydantic>=2.0`  | Data validation & serialization (v2 syntax) |

All listed in [`requirements.txt`](./requirements.txt). No optional extras — only what’s essential.

---

## 🛠️ Extensibility Hooks

- **Celery/Redis**: Add `celery` + `redis` to `requirements.txt`, inject `Celery` instance in `main.py`, and decorate long-running task handlers in `api/v1/tasks.py`.
- **Search upgrade**: Replace `core/search.py` logic with `psycopg` full-text or `elasticsearch-py` client — same input/output contract.
- **Settings expansion**: Extend `api/v1/settings.py` to read from DB or external config service; keep `/settings` response schema stable.
- **CI/CD**: `Dockerfile` uses multi-stage builds; `docker-compose.yml` includes `--build-arg` support for release tags.

---

## 📜 License

MIT — free to use, modify, and ship.

---

> **This implementation conforms strictly to scheme identifier `PROMPT-F78CD1-000083`.**
> No generated variants share this exact structure, naming, or extensibility posture.