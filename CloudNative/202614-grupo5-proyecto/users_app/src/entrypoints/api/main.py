from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.database.session import init_models
from config import Settings
from entrypoints.api.routers.user_router import router as user_router
from errors import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserNotVerifiedError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database schema before the application starts serving requests."""
    await init_models()
    yield


app = FastAPI(title=Settings().app_name, lifespan=lifespan)
app.include_router(user_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate FastAPI's default 422 request validation errors into 400, per API spec."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    """Return 412 when a user with the same username or email already exists."""
    return JSONResponse(status_code=412, content={})


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    """Return 404 when a user cannot be found by its id."""
    return JSONResponse(status_code=404, content={})


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    """Return 404 when the given username/password do not match any user."""
    return JSONResponse(status_code=404, content={})


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(
    request: Request, exc: InvalidTokenError
) -> JSONResponse:
    """Return 401 when a bearer token is missing from storage or has expired."""
    return JSONResponse(status_code=401, content={})


@app.exception_handler(UserNotVerifiedError)
async def user_not_verified_handler(
    request: Request, exc: UserNotVerifiedError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={})
