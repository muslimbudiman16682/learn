from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from sqlalchemy import DateTime
from typing import TYPE_CHECKING

from app.models.base import get_datetime_utc

if TYPE_CHECKING:
    from app.models.roles.role import Role


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
    is_protected: bool = Field(default=False, description="Prevent deletion if True")
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=...  # kept link model in migration
    )
