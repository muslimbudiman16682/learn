import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import get_datetime_utc

if TYPE_CHECKING:
    from app.models.items.item import Item
    from app.models.roles.role import Role


# Shared properties (used by both the table model and the API schemas)
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Database model, table name inferred from class name ("user")
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    role_id: uuid.UUID | None = Field(
        default=None, foreign_key="role.id", ondelete="SET NULL"
    )
    role: Optional["Role"] = Relationship(back_populates="users")
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
