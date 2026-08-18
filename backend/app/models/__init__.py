"""
Aggregates every domain's table models so SQLAlchemy/Alembic can see the
full schema.

IMPORTANT: when you add a new domain under models/<domain>/, import its
table model(s) here too -- otherwise Alembic autogenerate and
SQLModel.metadata will silently miss that table.
"""

from sqlmodel import SQLModel

from app.models.auths.role_permission import RolePermission
from app.models.auths.permission import Permission, PermissionBase
from app.models.auths.role import Role, RoleBase
from app.models.auths.user import User, UserBase

__all__ = [
    "SQLModel",
    "User",
    "UserBase",
    "Role",
    "RoleBase",
    "Permission",
    "PermissionBase",
    "RolePermission",
]
