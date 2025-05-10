from fastapi import (
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_services import AuthService, oauth2_scheme
from src.services.user_services import UserService
from src.database.db import get_db


def get_auth_service(db: AsyncSession = Depends(get_db)):
    """Get auth service."""
    return AuthService(db)


def get_user_service(db: AsyncSession = Depends(get_db)):
    """Get user service."""
    return UserService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get current user."""
    return await auth_service.get_current_user(token)