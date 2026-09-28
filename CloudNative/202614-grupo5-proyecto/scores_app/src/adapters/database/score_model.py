from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database.base import Base


class ScoreModel(Base):
    """Score database model."""

    __tablename__ = "scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    offer_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    size: Mapped[str] = mapped_column(String(10), nullable=False)
    offer: Mapped[float] = mapped_column(Float, nullable=False)
    bag_cost: Mapped[float] = mapped_column(Float, nullable=False)
    utility: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
