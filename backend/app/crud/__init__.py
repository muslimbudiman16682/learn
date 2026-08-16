"""
Re-exports every domain's CRUD functions so `from app import crud` keeps
working the way it did with the old single crud.py file. Add each new
domain's module here too.
"""

from app.crud.items import create_item
from app.crud.users import (
    DUMMY_HASH,
    authenticate,
    create_user,
    get_user_by_email,
    update_user,
)

__all__ = [
    "create_item",
    "DUMMY_HASH",
    "authenticate",
    "create_user",
    "get_user_by_email",
    "update_user",
]
