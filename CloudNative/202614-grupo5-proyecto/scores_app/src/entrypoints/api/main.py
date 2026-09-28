from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.database.session import init_models
from config import settings
from entrypoints.api.routers.score_router import router as score_router
from errors import InvalidScoreError, ScoreNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database schema before the application starts serving requests."""
    await init_models()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(score_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate FastAPI's default 422 request validation errors into 400, per API spec."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(InvalidScoreError)
async def invalid_score_handler(
    request: Request, exc: InvalidScoreError
) -> JSONResponse:
    """Return 412 when the score's input values are outside the expected range."""
    return JSONResponse(status_code=412, content={"msg": exc.message})


@app.exception_handler(ScoreNotFoundError)
async def score_not_found_handler(
    request: Request, exc: ScoreNotFoundError
) -> JSONResponse:
    """Return 404 when an offer has no score calculated yet."""
    return JSONResponse(status_code=404, content={})
