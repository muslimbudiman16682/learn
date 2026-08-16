"""
Business-logic orchestration for the permissions domain.
"""

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.models.permissions.permission import Permission
from app.schemas.permissions.permission import PermissionCreate


def create_permission(
    *, session: Session, permission_in: PermissionCreate
) -> Permission:
    if crud.get_permission_by_code(session=session, code=permission_in.code):
        raise HTTPException(
            status_code=400, detail="A permission with this code already exists"
        )
    return crud.create_permission(session=session, permission_in=permission_in)
