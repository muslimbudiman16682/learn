# app/models/roles/role_permission_link.py

import uuid

from sqlmodel import Field, SQLModel


class RolePermissionLink(SQLModel, table=True):
    role_id: uuid.UUID = Field(
        foreign_key="role.id",
        primary_key=True,
    )

    permission_id: uuid.UUID = Field(
        foreign_key="permission.id",
        primary_key=True,
    )