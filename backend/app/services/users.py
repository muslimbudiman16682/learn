"""
Business-logic orchestration for the users domain: combines crud calls,
validation rules, and side effects (like sending emails) that don't belong
in either the data-access layer (crud) or the HTTP layer (routes).
"""

import uuid

from fastapi import HTTPException
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models.auths.user import User
from app.schemas.auths.user import UserCreate, UserRegister
from app.utils import generate_new_account_email, send_email


def register_user(*, session: Session, user_in: UserRegister) -> User:
    """Public self-signup: no admin privileges required."""
    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    return crud.create_user(session=session, user_create=user_create)


def create_user_as_admin(*, session: Session, user_in: UserCreate) -> User:
    """Admin-only creation; also sends the new-account welcome email."""
    if crud.get_user_by_email(session=session, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        # generate_new_account_email expects (email_to, username, password)
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


def assert_email_available(
    *, session: Session, email: str, exclude_user_id: uuid.UUID | None = None
) -> None:
    """Raise 409 if another user already has this email."""
    existing_user = crud.get_user_by_email(session=session, email=email)
    if existing_user and existing_user.id != exclude_user_id:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )

