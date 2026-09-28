from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from assembly import build_create_post_rf003_use_case
from domain.use_cases.create_post_rf003_use_case import CreatePostRf003UseCase
from entrypoints.api.schemas.rf003_schemas import (
    CreatePublicationRequest,
    Rf003Response,
)

router = APIRouter(prefix="/rf003")
bearer_scheme = HTTPBearer(auto_error=False)


@router.post(
    "/posts",
    response_model=Rf003Response,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_publication_rf003(
    body: CreatePublicationRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    use_case: CreatePostRf003UseCase = Depends(build_create_post_rf003_use_case),
) -> Rf003Response:
    """RF-003: Crear publicación"""
    token = credentials.credentials if credentials else None
    post = await use_case.execute(token=token, data=body.to_command())
    return Rf003Response.from_publication(post)
