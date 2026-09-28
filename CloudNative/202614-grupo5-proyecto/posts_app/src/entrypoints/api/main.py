from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.database.session import init_models
from config import settings
from entrypoints.api.routers.post_router import router as post_router
from errors import ExpirationDateNoValid, PostNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database schema before the application starts serving requests."""
    await init_models()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(post_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate FastAPI's default 422 request validation errors into 400, per API spec."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(ExpirationDateNoValid)
async def expiration_date_validation_handler(
    request: Request, exc: ExpirationDateNoValid
) -> JSONResponse:
    """Return 412 when the expiration date is not valid."""
    return JSONResponse(status_code=412, content={"msg": exc.message})


@app.exception_handler(PostNotFoundError)
async def post_not_found_handler(
    request: Request, exc: PostNotFoundError
) -> JSONResponse:
    """Return 404 when a post cannot be found by its id."""
    return JSONResponse(status_code=404, content={})
