from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.package import Package

router = APIRouter(prefix="/packages", tags=["packages"])


class PackageCreate(BaseModel):
    name: str
    price: Decimal
    duration_seconds: int


@router.get("/")
def list_packages(db: Session = Depends(get_db)):
    return db.query(Package).order_by(Package.duration_seconds).all()


@router.post("/")
def create_package(payload: PackageCreate, db: Session = Depends(get_db)):
    package = Package(**payload.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return package
