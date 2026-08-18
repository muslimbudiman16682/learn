"""
Add each new domain's schema exports here as you create them, so imports
like `from app.schemas import XyzCreate` keep working project-wide.
"""

from app.schemas.common import Message, NewPassword, Token, TokenPayload
from app.schemas.auths.permission import (
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    PermissionUpdate,
)
from app.schemas.auths.role import (
    RoleCreate,
    RolePermissionsAssign,
    RolePublic,
    RolesPublic,
    RoleUpdate,
)
from app.schemas.auths.user import (
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
    "PermissionCreate",
    "PermissionPublic",
    "PermissionsPublic",
    "PermissionUpdate",
    "RoleCreate",
    "RolePermissionsAssign",
    "RolePublic",
    "RolesPublic",
    "RoleUpdate",
    "UpdatePassword",
    "UserCreate",
    "UserPublic",
    "UserRegister",
    "UsersPublic",
    "UserUpdate",
    "UserUpdateMe",
]
