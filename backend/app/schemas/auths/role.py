import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
    )


class RoleCreate(RoleBase):
    is_protected: bool = False


class RoleUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    description: str | None = Field(
        default=None,
        max_length=255,
    )
    is_protected: bool | None = None


class RolePublic(RoleBase):
    id: uuid.UUID
    is_protected: bool
    created_at: datetime