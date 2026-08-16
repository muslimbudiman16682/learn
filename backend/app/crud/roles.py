import uuid

from sqlmodel import Session, col, select

from app.models.permissions.permission import Permission
from app.models.roles.role import Role
from app.schemas.roles.role import RoleCreate, RoleUpdate


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
    *, session: Session, db_role: Role, permission_ids: list[uuid.UUID]
) -> Role:
    permissions = (
        session.exec(
            select(Permission).where(col(Permission.id).in_(permission_ids))
        ).all()
        if permission_ids
        else []
    )
    db_role.permissions = list(permissions)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role
