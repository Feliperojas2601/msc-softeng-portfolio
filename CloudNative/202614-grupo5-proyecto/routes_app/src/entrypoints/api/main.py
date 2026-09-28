from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.database.session import init_models
from config import settings
from entrypoints.api.routers.routes_router import router as routes_router
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables before accepting requests."""
    await init_models()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(routes_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Translate validation errors from 422 to the contract's 400."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(RouteAlreadyExistsError)
async def route_already_exists_handler(
    request: Request, exc: RouteAlreadyExistsError
) -> JSONResponse:
    """Return 412 when flightId already exists."""
    return JSONResponse(status_code=412, content={})


@app.exception_handler(InvalidRouteDatesError)
async def invalid_route_dates_handler(
    request: Request, exc: InvalidRouteDatesError
) -> JSONResponse:
    """Return 412 when the planned dates are invalid."""
    return JSONResponse(
        status_code=412,
        content={"msg": "Las fechas del trayecto no son válidas"},
    )


@app.exception_handler(RouteNotFoundError)
async def route_not_found_handler(
    request: Request, exc: RouteNotFoundError
) -> JSONResponse:
    """Return 404 when a route does not exist."""
    return JSONResponse(status_code=404, content={})
