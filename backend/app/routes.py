"""
routes.py

Defines API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Customer, Payment
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


def get_db():
    """Provide database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PaymentIn(BaseModel):
    account_number: str
    amount: float


@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    """Retrieve all customers."""
    return db.query(Customer).all()


@router.post("/payments")
def make_payment(payment_in: PaymentIn, db: Session = Depends(get_db)):
    """Make an EMI payment."""
    customer = db.query(Customer).filter_by(
        account_number=payment_in.account_number
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    payment = Payment(
        customer_id=customer.id,
        payment_amount=payment_in.amount,
        payment_date=datetime.utcnow(),
        status="SUCCESS"
    )
    try:
        db.add(payment)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Payment successful", "payment_id": payment.id}


@router.get("/payments/{account_number}")
def get_payments(account_number: str, db: Session = Depends(get_db)):
    """Retrieve payment history."""
    customer = db.query(Customer).filter_by(
        account_number=account_number
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.query(Payment).filter_by(
        customer_id=customer.id
    ).all()
