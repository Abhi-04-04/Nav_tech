"""
main.py

Application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import engine
from app.models import Base

app = FastAPI(title="Loan Payment API")

# Enable CORS for local dev and deployed frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Create tables if they don't exist (convenience for local dev)
    # If the database is unreachable (e.g., external DB not provisioned yet),
    # don't let the entire app fail at startup — log and continue.
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:  # broad catch to avoid startup failure in deployment
        import logging
        logging.warning("Database unavailable at startup, continuing without creating tables: %s", exc)

app.include_router(router)
