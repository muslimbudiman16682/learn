import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.roles.role import RoleBase
from app.schemas.permissions.permission import PermissionPublic


class RoleCreate(RoleBase):
    pass


class RoleUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RolePublic(RoleBase):
    id: uuid.UUID
    created_at: datetime | None = None
    permissions: list[PermissionPublic] = []


class RolesPublic(SQLModel):
    data: list[RolePublic]
    count: int


class RolePermissionsAssign(SQLModel):
    """Body for PUT /roles/{role_id}/permissions -- replaces the full set."""

    permission_ids: list[uuid.UUID]
