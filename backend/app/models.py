"""
models.py

Defines database models.
"""

from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    """Customer loan details."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    account_number = Column(String, unique=True, nullable=False)
    issue_date = Column(Date, nullable=False)
    interest_rate = Column(Numeric, nullable=False)
    tenure = Column(Integer, nullable=False)
    emi_due = Column(Numeric, nullable=False)


class Payment(Base):
    """Payment history."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_amount = Column(Numeric, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
