from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Router(Base):
    __tablename__ = "routers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    management_address: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(32), default="offline")

    sessions = relationship("Session", back_populates="router")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    router_id: Mapped[int | None] = mapped_column(ForeignKey("routers.id"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    customer = relationship("Customer", back_populates="sessions")
    router = relationship("Router", back_populates="sessions")
