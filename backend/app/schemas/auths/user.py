import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import BaseModel, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = Field(
        default=None,
        max_length=255,
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(
        default=None,
        max_length=255,
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )
    is_active: bool | None = None


class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    is_superuser: bool
    role_id: uuid.UUID | None = None
    created_at: datetime


class UserInDB(UserPublic):
    hashed_password: str