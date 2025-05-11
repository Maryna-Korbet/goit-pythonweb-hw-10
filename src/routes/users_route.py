from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status,
    BackgroundTasks,
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
    get_user_service,
)
from src.services.user_services import UserService
from src.schemas.email_schema import RequestEmail
from src.services.email_services import send_email
from src.core.email_token import get_email_from_token


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


@router.get("/confirmed_email/{token}")
async def confirmed_email(
    token: str, user_service: UserService = Depends(get_user_service)
):
    """Confirmed email."""
    email = get_email_from_token(token)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Verification error"
        )
    if user.confirmed:
        return {"message": messages.email_already_confirmed.get("en")}
    await user_service.confirmed_email(email)
    return {"message": messages.email_confirmed.get("en")}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    """Request email."""
    user = await user_service.get_user_by_email(str(body.email))

    if user.confirmed:
        return {"message": messages.email_already_confirmed.get("en")}
    if user:
        background_tasks.add_task(
            send_email, 
            user.email, 
            user.username, 
            str(request.base_url)
        )
    return {"message": messages.email_confirm_request.get("en")}


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