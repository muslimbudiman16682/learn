"""
Re-exports every domain's CRUD functions so `from app import crud` keeps
working the way it did with the old single crud.py file. Add each new
domain's module here too.
"""


from app.crud.permissions import (
    create_permission,
    delete_permission,
    get_permission,
    get_permission_by_code,
    update_permission,
)
from app.crud.roles import (
    create_role,
    delete_role,
    get_role,
    get_role_by_name,
    set_role_permissions,
    update_role,
)
from app.crud.users import (
    DUMMY_HASH,
    authenticate,
    create_user,
    get_user_by_email,
    update_user,
)

__all__ = [
    "create_item",
    "create_permission",
    "delete_permission",
    "get_permission",
    "get_permission_by_code",
    "update_permission",
    "create_role",
    "delete_role",
    "get_role",
    "get_role_by_name",
    "set_role_permissions",
    "update_role",
    "DUMMY_HASH",
    "authenticate",
    "create_user",
    "get_user_by_email",
    "update_user",
]
