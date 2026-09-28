from fastapi import APIRouter, Depends

from assembly import build_process_verification_callback_use_case
from domain.use_cases.process_verification_callback_use_case import (
    ProcessVerificationCallbackUseCase,
)
from entrypoints.api.schemas.verification_schemas import VerifyCallbackRequest

router = APIRouter()


@router.patch("/verify-callback")
async def verify_callback(
    body: VerifyCallbackRequest,
    use_case: ProcessVerificationCallbackUseCase = Depends(
        build_process_verification_callback_use_case
    ),
) -> dict:
    """Receive TrueNative's identity verification callback (RF-007).

    Always responds 200 on a structurally valid request, per TrueNative's
    contract; an invalid signature is acknowledged without being acted on
    (see the InvalidSignatureError handler in main.py).
    """
    await use_case.execute(
        ruv=body.RUV,
        user_id=body.userIdentifier,
        status=body.status,
        score=body.score,
        verify_token=body.verifyToken,
    )
    return {"msg": "ok"}
