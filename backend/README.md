# Backend (FastAPI)

Run locally:

1. Activate virtualenv and install requirements:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create DB tables (optional; startup will auto-create):

```powershell
python scripts\init_db.py
```

3. Start dev server:

```powershell
python -m uvicorn app.main:app --reload
```

Notes:
- Configure DB using `DATABASE_URL` env var (e.g., `postgresql://user:pass@host:5432/loan_db`).
- CORS middleware is enabled (currently allow_origins=`*` for dev).
