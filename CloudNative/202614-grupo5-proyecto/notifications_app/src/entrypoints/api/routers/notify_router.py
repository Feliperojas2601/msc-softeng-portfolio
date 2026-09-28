from fastapi import APIRouter, Depends

from assembly import build_send_notification_use_case
from domain.use_cases.send_notification_use_case import SendNotificationUseCase
from entrypoints.api.schemas.notify_schemas import NotifyRequest

router = APIRouter()


@router.post("/notify")
async def notify(
    body: NotifyRequest,
    use_case: SendNotificationUseCase = Depends(build_send_notification_use_case),
) -> dict:
    """Receive a result notification and publish it (RF-006 and RF-007)."""
    await use_case.execute(
        type=body.type,
        user_id=body.userId,
        email=body.email,
        full_name=body.fullName,
        status=body.status,
        ruv=body.ruv,
        last_four_digits=body.lastFourDigits,
        franchise=body.franchise,
    )
    return {"msg": "ok"}
