from sqlmodel import Session, col, select
from typing import List
import uuid

from fastapi import HTTPException

from app.models.auths.permission import Permission
from app.models.auths.role import Role
from app.schemas.auths.role import RoleCreate, RoleUpdate


def create_role(*, session: Session, role_in: RoleCreate) -> Role:
    db_role = Role.model_validate(role_in)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


def get_role(*, session: Session, role_id: uuid.UUID) -> Role | None:
    return session.get(Role, role_id)


def get_role_by_name(*, session: Session, name: str) -> Role | None:
    statement = select(Role).where(Role.name == name)
    return session.exec(statement).first()


def update_role(*, session: Session, db_role: Role, role_in: RoleUpdate) -> Role:
    update_data = role_in.model_dump(exclude_unset=True)
    db_role.sqlmodel_update(update_data)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


def delete_role(*, session: Session, db_role: Role) -> None:
    session.delete(db_role)
    session.commit()


def set_role_permissions(
    *, session: Session, db_role: Role, permission_ids: List[uuid.UUID]
) -> Role:
    # Fetch existing permissions for provided IDs
    permissions = (
        session.exec(
            select(Permission).where(col(Permission.id).in_(permission_ids))
        ).all()
        if permission_ids
        else []
    )

    found_ids = {p.id for p in permissions}
    missing = [str(pid) for pid in permission_ids if pid not in found_ids]
    if missing:
        raise HTTPException(status_code=400, detail=f"Invalid permission_ids: {missing}")

    db_role.permissions = list(permissions)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

