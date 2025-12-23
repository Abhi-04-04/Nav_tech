# Backend (FastAPI) ✅

A small FastAPI service that provides customer and payment endpoints used by the frontends.

Quick start (Windows):

1. Create & activate a virtual environment and install requirements:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Create database tables (the app attempts this on startup):

```powershell
python scripts\init_db.py
```

3. Run the app in development:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Environment
- Set `DATABASE_URL` to your Postgres connection (example):
  `postgresql://user:pass@host:5432/loan_db`
- The app will try to create tables on startup; if the DB is unreachable it will continue running and return `503` for DB-dependent endpoints.

Notes & deploy
- CORS is enabled (`allow_origins="*"`) for development — tighten this in production.
- For deployment we use `systemd` + `nginx`. See the `deploy/` folder for service and nginx templates.
- There is a Streamlit UI in `frontend_streamlit/` that talks to this API.
