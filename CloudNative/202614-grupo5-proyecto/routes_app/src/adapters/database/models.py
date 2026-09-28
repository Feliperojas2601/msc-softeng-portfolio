from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database.session import Base


class RouteModel(Base):
    """SQLAlchemy ORM model for the routes table."""

    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    flight_id: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    source_airport_code: Mapped[str] = mapped_column(String(3), nullable=False)
    source_country: Mapped[str] = mapped_column(String, nullable=False)
    destiny_airport_code: Mapped[str] = mapped_column(String(3), nullable=False)
    destiny_country: Mapped[str] = mapped_column(String, nullable=False)
    bag_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    planned_start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    planned_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
