import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc


if TYPE_CHECKING:
    from app.models.auths.role import Role


class UserBase(SQLModel):
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
    )

    is_active: bool = True
    is_superuser: bool = False

    full_name: str | None = Field(
        default=None,
        max_length=255,
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    hashed_password: str

    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    role_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="role.id",
        ondelete="SET NULL",
    )

    role: Optional["Role"] = Relationship(
        back_populates="users",
    )

