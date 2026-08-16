import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc

if TYPE_CHECKING:
    from app.models.roles.role import Role


class RolePermissionLink(SQLModel, table=True):
    """Join table: which permissions a role grants."""

    __tablename__ = "role_permission_link"

    role_id: uuid.UUID = Field(
        foreign_key="role.id", primary_key=True, ondelete="CASCADE"
    )
    permission_id: uuid.UUID = Field(
        foreign_key="permission.id", primary_key=True, ondelete="CASCADE"
    )


class PermissionBase(SQLModel):
    # e.g. "items:create", "users:delete" -- namespaced so 100 domains stay collision-free
    code: str = Field(unique=True, index=True, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class Permission(PermissionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )
