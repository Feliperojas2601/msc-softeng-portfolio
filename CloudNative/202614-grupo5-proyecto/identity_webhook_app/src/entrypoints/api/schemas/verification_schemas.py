from pydantic import BaseModel, ConfigDict


class VerifyCallbackRequest(BaseModel):
    """Request body TrueNative sends to PATCH /verify-callback."""

    model_config = ConfigDict(populate_by_name=True)

    RUV: str
    userIdentifier: str
    createdAt: str | None = None
    status: str
    score: float
    verifyToken: str
