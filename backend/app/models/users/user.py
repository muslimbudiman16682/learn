import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, TIMESTAMP
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc


if TYPE_CHECKING:
    from app.models.items.item import Item
    from app.models.roles.role import Role


class UserBase(SQLModel):
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
        sa_type=str,
    )
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(
        default=None,
        max_length=255,
    )


class User(UserBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    hashed_password: str

    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )

    role_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="role.id",
        ondelete="SET NULL",
        nullable=True,
    )

    role: "Role | None" = Relationship(
        back_populates="users",
    )

    items: list["Item"] = Relationship(
        back_populates="owner",
    )