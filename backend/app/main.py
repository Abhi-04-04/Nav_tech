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
    Base.metadata.create_all(bind=engine)

app.include_router(router)
