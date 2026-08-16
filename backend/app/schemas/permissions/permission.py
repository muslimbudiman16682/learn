import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.permissions.permission import PermissionBase


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(SQLModel):
    code: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class PermissionPublic(PermissionBase):
    id: uuid.UUID
    created_at: datetime | None = None


class PermissionsPublic(SQLModel):
    data: list[PermissionPublic]
    count: int
