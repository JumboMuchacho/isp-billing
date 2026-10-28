from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import AuditLog, Subscription
from app.models.session import Router
from app.services.billing_service import BillingService

router = APIRouter(prefix="/admin", tags=["admin"])
billing = BillingService()


class RouterCreate(BaseModel):
    name: str
    management_address: str
    status: str = "offline"


class AuditLogCreate(BaseModel):
    actor: str
    action: str


@router.get("/routers")
def list_routers(db: Session = Depends(get_db)):
    return db.query(Router).all()


@router.post("/routers")
def create_router(payload: RouterCreate, db: Session = Depends(get_db)):
    device = Router(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()


@router.post("/audit-logs")
def create_audit_log(payload: AuditLogCreate, db: Session = Depends(get_db)):
    log = AuditLog(**payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/subscriptions")
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()


@router.post("/subscriptions/expire")
def expire_subscriptions(db: Session = Depends(get_db)):
    expired = billing.expire_due_subscriptions(db)
    return {"expired": len(expired), "ids": [item.id for item in expired]}
