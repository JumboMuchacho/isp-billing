from collections.abc import Generator
from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DEFAULT_PACKAGES = [
    {"name": "1 hour", "price": Decimal("10.00"), "duration_seconds": 3600},
    {"name": "3 hours", "price": Decimal("20.00"), "duration_seconds": 10800},
    {"name": "12 hours", "price": Decimal("25.00"), "duration_seconds": 43200},
    {"name": "24 hours", "price": Decimal("35.00"), "duration_seconds": 86400},
    {"name": "3 days", "price": Decimal("110.00"), "duration_seconds": 259200},
    {"name": "1 week", "price": Decimal("230.00"), "duration_seconds": 604800},
]


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_packages(db: Session) -> None:
    from app.models.package import Package

    existing = {row.name for row in db.scalars(select(Package)).all()}
    for package in DEFAULT_PACKAGES:
        if package["name"] not in existing:
            db.add(Package(**package))
    db.commit()


def init_db() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_packages(db)
    finally:
        db.close()
