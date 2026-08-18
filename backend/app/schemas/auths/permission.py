import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
    )


class PermissionCreate(PermissionBase):
    is_protected: bool = False


class PermissionUpdate(BaseModel):
    code: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    is_protected: bool | None = None


class PermissionPublic(PermissionBase):
    id: uuid.UUID
    is_protected: bool
    created_at: datetime