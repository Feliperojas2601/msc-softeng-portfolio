from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from assembly import (
    build_authenticate_user_use_case,
    build_count_users_use_case,
    build_create_user_use_case,
    build_get_current_user_use_case,
    build_get_user_by_id_use_case,
    build_reset_users_use_case,
    build_update_user_use_case,
)
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from domain.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from domain.use_cases.reset_users_use_case import ResetUsersUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase
from entrypoints.api.schemas.user_schemas import (
    AuthRequest,
    AuthResponse,
    CountResponse,
    CreateUserRequest,
    CreateUserResponse,
    MeResponse,
    MessageResponse,
    UpdateUserRequest,
)

router = APIRouter(prefix="/users")
bearer_scheme = HTTPBearer(auto_error=False)


@router.post("", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(build_create_user_use_case),
) -> CreateUserResponse:
    """Create a new user with a unique username and email."""
    user = await use_case.execute(
        username=body.username,
        password=body.password,
        email=body.email,
        dni=body.dni,
        full_name=body.full_name,
        phone_number=body.phone_number,
    )
    return CreateUserResponse.from_user(user)


@router.patch("/{user_id}", response_model=MessageResponse)
async def update_user(
    user_id: str,
    body: UpdateUserRequest,
    use_case: UpdateUserUseCase = Depends(build_update_user_use_case),
) -> MessageResponse:
    """Update the mutable fields of an existing user."""
    await use_case.execute(
        user_id=user_id,
        status=body.status,
        dni=body.dni,
        full_name=body.full_name,
        phone_number=body.phone_number,
    )
    return MessageResponse(msg="el usuario ha sido actualizado")


@router.post("/auth", response_model=AuthResponse)
async def authenticate_user(
    body: AuthRequest,
    use_case: AuthenticateUserUseCase = Depends(build_authenticate_user_use_case),
) -> AuthResponse:
    """Generate a new session token for a user matching the given credentials."""
    user = await use_case.execute(username=body.username, password=body.password)
    return AuthResponse.from_user(user)


@router.get("/me", response_model=MeResponse)
async def get_me(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    use_case: GetCurrentUserUseCase = Depends(build_get_current_user_use_case),
) -> MeResponse:
    """Return the data of the user owning the given bearer token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )
    user = await use_case.execute(credentials.credentials)
    return MeResponse.from_user(user)


@router.get("/count", response_model=CountResponse)
async def count_users(
    use_case: CountUsersUseCase = Depends(build_count_users_use_case),
) -> CountResponse:
    """Return how many users are currently stored."""
    count = await use_case.execute()
    return CountResponse(count=count)


@router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    """Healthcheck endpoint."""
    return "pong"


@router.get("/{user_id}", response_model=MeResponse)
async def get_user_by_id(
    user_id: str,
    use_case: GetUserByIdUseCase = Depends(build_get_user_by_id_use_case),
) -> MeResponse:
    """Return the public data of a user by its id.

    Public by architectural decision, mirroring PATCH /users/{id}: internal
    components (e.g. the identity verification webhook) need to read a user's
    contact data to build notifications, and per the project's ownership rule
    that data can only be obtained through the API of the app that owns it.
    """
    user = await use_case.execute(user_id)
    return MeResponse.from_user(user)


@router.post("/reset", response_model=MessageResponse)
async def reset_users(
    use_case: ResetUsersUseCase = Depends(build_reset_users_use_case),
) -> MessageResponse:
    """Delete every stored user."""
    await use_case.execute()
    return MessageResponse(msg="Todos los datos fueron eliminados")
