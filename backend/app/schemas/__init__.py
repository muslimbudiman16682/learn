"""
Add each new domain's schema exports here as you create them, so imports
like `from app.schemas import XyzCreate` keep working project-wide.
"""

from app.schemas.common import Message, NewPassword, Token, TokenPayload
from app.schemas.items.item import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.schemas.users.user import (
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

__all__ = [
    "Message",
    "NewPassword",
    "Token",
    "TokenPayload",
    "ItemCreate",
    "ItemPublic",
    "ItemsPublic",
    "ItemUpdate",
    "UpdatePassword",
    "UserCreate",
    "UserPublic",
    "UserRegister",
    "UsersPublic",
    "UserUpdate",
    "UserUpdateMe",
]
