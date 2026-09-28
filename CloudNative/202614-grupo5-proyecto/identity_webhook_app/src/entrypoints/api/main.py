from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import settings
from entrypoints.api.routers.health_router import router as health_router
from entrypoints.api.routers.verification_router import router as verification_router
from errors import DownstreamUnavailableError, InvalidSignatureError, UserNotFoundError

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(verification_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate FastAPI's default 422 request validation errors into 400."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(InvalidSignatureError)
async def invalid_signature_handler(
    request: Request, exc: InvalidSignatureError
) -> JSONResponse:
    """Acknowledge an untrusted callback with 200 without acting on it.

    TrueNative's contract requires responding 200 to every structurally
    valid callback; an invalid signature means we don't trust it enough to
    update anything, but we still acknowledge receipt.
    """
    return JSONResponse(status_code=200, content={"msg": "ignored"})


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    """Return 500: users_app has no user matching a RUV we generated ourselves."""
    return JSONResponse(status_code=500, content={"msg": "user not found"})


@app.exception_handler(DownstreamUnavailableError)
async def downstream_unavailable_handler(
    request: Request, exc: DownstreamUnavailableError
) -> JSONResponse:
    """Return 502 when users_app could not be reached to apply the result."""
    return JSONResponse(status_code=502, content={"msg": "downstream unavailable"})
