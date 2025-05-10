from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from src.services.auth_services import (
    AuthService,
    oauth2_scheme,
)
from src.schemas.user_schema import (
    UserResponse,
)

from src.core.depend_service import (
    get_auth_service,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def me(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get current user."""
    return await auth_service.get_current_user(token)
