"""
Aggregates every domain's table models so SQLAlchemy/Alembic can see the
full schema.

IMPORTANT: when you add a new domain under models/<domain>/, import its
table model(s) here too -- otherwise Alembic autogenerate and
SQLModel.metadata will silently miss that table.
"""

from sqlmodel import SQLModel

from app.models.items.item import Item, ItemBase
from app.models.users.user import User, UserBase

__all__ = [
    "SQLModel",
    "User",
    "UserBase",
    "Item",
    "ItemBase",
]
