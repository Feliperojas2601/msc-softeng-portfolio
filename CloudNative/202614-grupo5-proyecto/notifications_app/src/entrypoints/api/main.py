from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import settings
from entrypoints.api.routers.health_router import router as health_router
from entrypoints.api.routers.notify_router import router as notify_router
from errors import NotificationPublishError

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(notify_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate FastAPI's default 422 request validation errors into 400."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(NotificationPublishError)
async def notification_publish_error_handler(
    request: Request, exc: NotificationPublishError
) -> JSONResponse:
    """Return 502 when the notification could not be published (e.g., SNS unreachable)."""
    return JSONResponse(status_code=502, content={"msg": "notification unavailable"})
