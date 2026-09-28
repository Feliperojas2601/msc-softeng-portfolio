from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import settings
from entrypoints.api.routers.health_router import router as health_router
from entrypoints.api.routers.proxy_router import router as proxy_router
from entrypoints.api.routers.rf003_router import router as rf003_router
from entrypoints.api.routers.rf004_router import router as rf004_router
from entrypoints.api.routers.rf005_router import router as rf005_router
from errors import OrchestratorError

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(rf003_router)
app.include_router(rf004_router)
app.include_router(rf005_router)
# La siguiente linea es para probar los requerimientos en local
# app.include_router(proxy_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Traduce cualquier error de validación de Pydantic en un código de estado HTTP 400 con un cuerpo de mensaje legible."""
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(OrchestratorError)
async def orchestrator_error_handler(
    request: Request, exc: OrchestratorError
) -> JSONResponse:
    """Maneja cualquier error de orquestador personalizado y devuelve un código de estado HTTP y un mensaje legible."""
    return JSONResponse(status_code=exc.status_code, content={"msg": exc.message})
