from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.package import Package
from app.models.payment import Payment
from app.services.billing_service import BillingService
from app.services.mpesa_service import MpesaService

router = APIRouter(prefix="/payments", tags=["payments"])
mpesa = MpesaService()
billing = BillingService()


class StkPushRequest(BaseModel):
    phone: str
    amount: str
    account_ref: str


class CompletePaymentRequest(BaseModel):
    phone: str
    package_id: int
    receipt: str


@router.get("/")
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.post("/mpesa/stk")
def initiate_stk(payload: StkPushRequest):
    return mpesa.initiate_stk_push(payload.phone, payload.amount, payload.account_ref)


@router.post("/mpesa/callback")
def mpesa_callback(payload: dict):
    return mpesa.handle_callback(payload)


@router.post("/complete")
def complete_payment(payload: CompletePaymentRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == payload.phone).one_or_none()
    if customer is None:
        customer = Customer(phone=payload.phone)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    package = db.get(Package, payload.package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    payment, subscription = billing.complete_purchase(
        db,
        customer,
        package,
        package.price,
        payload.receipt,
    )
    return {
        "payment_id": payment.id,
        "subscription_id": subscription.id,
        "status": payment.status,
        "started_at": subscription.started_at,
        "expires_at": subscription.expires_at,
        "duration_seconds": package.duration_seconds,
    }
