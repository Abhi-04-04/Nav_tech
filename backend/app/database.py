"""
database.py

Handles database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Allow overriding via environment variable for safer deployment & local testing
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:root@localhost:5433/loan_db"
)

# Enable pool_pre_ping to avoid stale/closed connection issues
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
