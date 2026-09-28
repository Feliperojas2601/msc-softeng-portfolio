from abc import ABC, abstractmethod

from domain.models.offer import Offer
from entrypoints.api.schemas.offer_filters import OfferFilters


class OfferRepositoryPort(ABC):
    """Offer repository interface."""

    @abstractmethod
    def create(self, offer: Offer) -> Offer:
        """Create a new offer."""

    @abstractmethod
    def get_by_id(self, offer_id: str) -> Offer | None:
        """Get offer by ID."""

    @abstractmethod
    def get_all(self, filters: OfferFilters) -> list[Offer]:
        """Get all offers matching the given filters."""

    @abstractmethod
    def delete(self, offer_id: str) -> bool:
        """Delete an offer."""

    @abstractmethod
    def count(self) -> int:
        """Return the number of offers."""

    @abstractmethod
    def reset(self) -> None:
        """Delete all offers."""
