from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer, Subscription
from app.models.package import Package
from app.models.payment import Payment
from app.services.radius_service import RadiusService


class BillingService:
    def __init__(self) -> None:
        self.radius = RadiusService()

    def is_active(self, subscription: Subscription, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        expires_at = subscription.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return subscription.status == "active" and expires_at > now

    def activate_subscription(
        self,
        db: Session,
        customer: Customer,
        package: Package,
        started_at: datetime | None = None,
    ) -> Subscription:
        started_at = started_at or datetime.now(timezone.utc)
        subscription = Subscription(
            customer_id=customer.id,
            package_id=package.id,
            started_at=started_at,
            expires_at=started_at + timedelta(seconds=package.duration_seconds),
            status="active",
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    def record_payment(
        self,
        db: Session,
        customer: Customer,
        package: Package,
        amount,
        receipt: str | None = None,
    ) -> Payment:
        payment = Payment(
            customer_id=customer.id,
            package_id=package.id,
            amount=amount,
            receipt=receipt,
            status="completed" if receipt else "pending",
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def complete_purchase(
        self,
        db: Session,
        customer: Customer,
        package: Package,
        amount,
        receipt: str,
    ) -> tuple[Payment, Subscription]:
        payment = self.record_payment(db, customer, package, amount, receipt)
        subscription = self.activate_subscription(db, customer, package)
        return payment, subscription

    def expire_due_subscriptions(self, db: Session, now: datetime | None = None) -> list[Subscription]:
        now = now or datetime.now(timezone.utc)
        due = db.scalars(
            select(Subscription).where(
                Subscription.status == "active",
                Subscription.expires_at <= now,
            )
        ).all()
        expired: list[Subscription] = []
        for subscription in due:
            subscription.status = "expired"
            customer = db.get(Customer, subscription.customer_id)
            if customer:
                self.radius.disconnect(customer.phone)
            expired.append(subscription)
        db.commit()
        return expired
