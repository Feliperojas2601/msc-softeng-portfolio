from typing import Literal

from pydantic import BaseModel, ConfigDict


class NotifyRequest(BaseModel):
    """Request body for POST /notify, sent by identity_webhook_app and credit_cards_app."""

    model_config = ConfigDict(populate_by_name=True)

    type: Literal["IDENTITY_VERIFICATION", "CREDIT_CARD_VERIFICATION"]
    userId: str
    email: str
    fullName: str | None = None
    status: str
    ruv: str
    lastFourDigits: str | None = None
    franchise: str | None = None
