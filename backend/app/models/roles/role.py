import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc
from app.models.permissions.permission import RolePermissionLink

if TYPE_CHECKING:
    from app.models.permissions.permission import Permission
    from app.models.users.user import User


class RoleBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class Role(RoleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    users: list["User"] = Relationship(back_populates="role")
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )
