import uuid

from sqlmodel import Session, select

from app.models.auths.permission import Permission
from app.schemas.auths.permission import PermissionCreate, PermissionUpdate


def create_permission(
    *, session: Session, permission_in: PermissionCreate
) -> Permission:
    db_permission = Permission.model_validate(permission_in)
    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)
    return db_permission


def get_permission(*, session: Session, permission_id: uuid.UUID) -> Permission | None:
    return session.get(Permission, permission_id)


def get_permission_by_code(*, session: Session, code: str) -> Permission | None:
    statement = select(Permission).where(Permission.code == code)
    return session.exec(statement).first()


def update_permission(
    *, session: Session, db_permission: Permission, permission_in: PermissionUpdate
) -> Permission:
    update_data = permission_in.model_dump(exclude_unset=True)
    db_permission.sqlmodel_update(update_data)
    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)
    return db_permission


def delete_permission(*, session: Session, db_permission: Permission) -> None:
    session.delete(db_permission)
    session.commit()

