import uuid

from sqlmodel import Field, SQLModel


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permission"

    role_id: uuid.UUID = Field(
        foreign_key="role.id",
        primary_key=True,
    )

    permission_id: uuid.UUID = Field(
        foreign_key="permission.id",
        primary_key=True,
    )