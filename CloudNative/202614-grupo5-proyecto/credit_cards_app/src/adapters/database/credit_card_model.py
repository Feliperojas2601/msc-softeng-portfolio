from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database.base import Base


class CreditCardModel(Base):
    __tablename__ = "credit_cards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    token: Mapped[str] = mapped_column(String(256), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    last_four_digits: Mapped[str] = mapped_column(String(4), nullable=False)
    ruv: Mapped[str | None] = mapped_column(String(256), nullable=True)
    issuer: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
