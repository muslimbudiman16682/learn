import uuid

from pydantic import BaseModel


class RolePermissionCreate(BaseModel):
    role_id: uuid.UUID
    permission_id: uuid.UUID


class RolePermissionPublic(BaseModel):
    role_id: uuid.UUID
    permission_id: uuid.UUID