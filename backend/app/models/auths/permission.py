import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc


if TYPE_CHECKING:
    from app.models.auths.role import Role
    from app.models.auths.role_permission import RolePermission


class PermissionBase(SQLModel):
    code: str = Field(
        unique=True,
        index=True,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )


class Permission(PermissionBase, table=True):
    __tablename__ = "permission"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    is_protected: bool = Field(
        default=False,
        description="Prevent deletion if True",
    )

    roles: list["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
    )