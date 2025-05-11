from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.services.auth_services import AuthService, oauth2_scheme
from src.schemas.user_schema import UserResponse
from src.entity.models import User
from src.config import messages
from src.core.depend_service import (
    get_auth_service,
    get_current_admin_user,
    get_current_moderator_user,
)


router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=UserResponse)
@limiter.limit("10/minute")
async def me(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get current user."""
    return await auth_service.get_current_user(token)


@router.get("/moderator")
def read_moderator(
    current_user: User = Depends(get_current_moderator_user),
):
    """Read moderator."""
    return {
        "message": messages.welcome_messages["moderator"]
        .get("en")
        .format(username=current_user.username)
    }


@router.get("/admin")
def read_admin(current_user: User = Depends(get_current_admin_user)):
    """Read admin."""
    return {
        "message": messages.welcome_messages["admin"]
        .get("en")
        .format(username=current_user.username)
    }