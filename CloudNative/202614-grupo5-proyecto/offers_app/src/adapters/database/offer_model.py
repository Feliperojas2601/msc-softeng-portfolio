from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database.base import Base


class OfferModel(Base):
    """Offer database model."""

    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    post_id: Mapped[str] = mapped_column(String(36), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String(10), nullable=False)
    fragile: Mapped[bool] = mapped_column(Boolean, nullable=False)
    offer: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
