import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models.permissions.permission import Permission
from app.schemas.common import Message
from app.schemas.permissions.permission import (
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    PermissionUpdate,
)
from app.services.permissions import create_permission as create_permission_service

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
    dependencies=[Depends(get_current_active_superuser)],
)


@router.get("/", response_model=PermissionsPublic)
def read_permissions(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve permissions.
    """
    count_statement = select(func.count()).select_from(Permission)
    count = session.exec(count_statement).one()
    statement = select(Permission).offset(skip).limit(limit)
    permissions = session.exec(statement).all()
    return PermissionsPublic(data=permissions, count=count)


@router.get("/{permission_id}", response_model=PermissionPublic)
def read_permission(session: SessionDep, permission_id: uuid.UUID) -> Any:
    """
    Get permission by ID.
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.post("/", response_model=PermissionPublic)
def create_permission(
    *, session: SessionDep, permission_in: PermissionCreate
) -> Any:
    """
    Create new permission.
    """
    return create_permission_service(session=session, permission_in=permission_in)


@router.patch("/{permission_id}", response_model=PermissionPublic)
def update_permission(
    *, session: SessionDep, permission_id: uuid.UUID, permission_in: PermissionUpdate
) -> Any:
    """
    Update a permission.
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    if permission_in.code and permission_in.code != permission.code:
        existing = session.exec(
            select(Permission).where(Permission.code == permission_in.code)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, detail="A permission with this code already exists"
            )
    update_dict = permission_in.model_dump(exclude_unset=True)
    permission.sqlmodel_update(update_dict)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


@router.delete("/{permission_id}")
def delete_permission(session: SessionDep, permission_id: uuid.UUID) -> Message:
    """
    Delete a permission.
    """
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    session.delete(permission)
    session.commit()
    return Message(message="Permission deleted successfully")
