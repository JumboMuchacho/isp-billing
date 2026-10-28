from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer

router = APIRouter(prefix="/customers", tags=["customers"])


class CustomerCreate(BaseModel):
    phone: str


@router.get("/")
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.post("/")
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(phone=payload.phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
