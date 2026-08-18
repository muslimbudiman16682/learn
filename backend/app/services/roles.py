"""
Business-logic orchestration for the roles domain.
"""

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.models.auths.role import Role
from app.schemas.auths.role import RoleCreate


def create_role(*, session: Session, role_in: RoleCreate) -> Role:
    if crud.get_role_by_name(session=session, name=role_in.name):
        raise HTTPException(
            status_code=400, detail="A role with this name already exists"
        )
    return crud.create_role(session=session, role_in=role_in)

