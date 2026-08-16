import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models.roles.role import Role
from app.schemas.common import Message
from app.schemas.roles.role import (
    RoleCreate,
    RolePermissionsAssign,
    RolePublic,
    RolesPublic,
    RoleUpdate,
)
from app.services.roles import create_role as create_role_service

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(get_current_active_superuser)],
)


@router.get("/", response_model=RolesPublic)
def read_roles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve roles.
    """
    count_statement = select(func.count()).select_from(Role)
    count = session.exec(count_statement).one()
    statement = select(Role).offset(skip).limit(limit)
    roles = session.exec(statement).all()
    return RolesPublic(data=roles, count=count)


@router.get("/{role_id}", response_model=RolePublic)
def read_role(session: SessionDep, role_id: uuid.UUID) -> Any:
    """
    Get role by ID.
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RolePublic)
def create_role(*, session: SessionDep, role_in: RoleCreate) -> Any:
    """
    Create new role.
    """
    return create_role_service(session=session, role_in=role_in)


@router.patch("/{role_id}", response_model=RolePublic)
def update_role(*, session: SessionDep, role_id: uuid.UUID, role_in: RoleUpdate) -> Any:
    """
    Update a role.
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if role_in.name and role_in.name != role.name:
        existing = session.exec(select(Role).where(Role.name == role_in.name)).first()
        if existing:
            raise HTTPException(
                status_code=400, detail="A role with this name already exists"
            )
    update_dict = role_in.model_dump(exclude_unset=True)
    role.sqlmodel_update(update_dict)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@router.put("/{role_id}/permissions", response_model=RolePublic)
def assign_role_permissions(
    *, session: SessionDep, role_id: uuid.UUID, body: RolePermissionsAssign
) -> Any:
    """
    Replace the full set of permissions granted by this role.
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud.set_role_permissions(
        session=session, db_role=role, permission_ids=body.permission_ids
    )


@router.delete("/{role_id}")
def delete_role(session: SessionDep, role_id: uuid.UUID) -> Message:
    """
    Delete a role.
    """
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    session.delete(role)
    session.commit()
    return Message(message="Role deleted successfully")
