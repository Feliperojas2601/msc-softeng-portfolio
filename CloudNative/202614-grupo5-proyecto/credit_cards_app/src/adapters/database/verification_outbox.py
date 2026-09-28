from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database.base import Base

POLLING_RETRY_SECONDS = 1
PROCESSING_LEASE_SECONDS = 60


class VerificationOutboxModel(Base):
    __tablename__ = "credit_card_verification_outbox"

    card_id: Mapped[str] = mapped_column(
        ForeignKey("credit_cards.id", ondelete="CASCADE"), primary_key=True
    )
    event_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    ruv: Mapped[str] = mapped_column(String(256), nullable=False)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    lease_id: Mapped[str | None] = mapped_column(String(36))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class VerificationOutboxRepository:
    def __init__(self, session):
        self.session = session

    def claim(self, card_id=None, limit=1):
        now = datetime.now(UTC)
        query = select(VerificationOutboxModel).where(
            VerificationOutboxModel.published_at.is_(None),
            VerificationOutboxModel.available_at <= now,
        )
        if card_id is not None:
            query = query.where(VerificationOutboxModel.card_id == card_id)
        rows = self.session.scalars(
            query.order_by(VerificationOutboxModel.available_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        ).all()
        events = []
        for row in rows:
            row.lease_id = str(uuid4())
            row.available_at = now + timedelta(seconds=PROCESSING_LEASE_SECONDS)
            events.append(
                {
                    "eventId": row.event_id,
                    "cardId": row.card_id,
                    "ruv": row.ruv,
                    "attempt": 0,
                    "leaseId": row.lease_id,
                }
            )
        self.session.commit()
        return events

    def release(self, event_id, lease_id):
        now = datetime.now(UTC)
        row = self.session.scalar(
            select(VerificationOutboxModel)
            .where(
                VerificationOutboxModel.event_id == event_id,
                VerificationOutboxModel.lease_id == lease_id,
                VerificationOutboxModel.published_at.is_(None),
                VerificationOutboxModel.available_at > now,
            )
            .with_for_update()
        )
        if row is None:
            return False
        row.lease_id = None
        row.available_at = now + timedelta(seconds=POLLING_RETRY_SECONDS)
        self.session.commit()
        return True

    def acknowledge(self, event_id, lease_id):
        row = self.session.scalar(
            select(VerificationOutboxModel)
            .where(VerificationOutboxModel.event_id == event_id)
            .with_for_update()
        )
        if row is None or row.lease_id != lease_id:
            return False
        if row.published_at is None:
            row.published_at = datetime.now(UTC)
            self.session.commit()
        return True
