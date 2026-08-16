"""
Business-logic orchestration for the items domain. Currently thin (items
have no extra rules beyond ownership, which api/deps.py already handles),
kept here as the reference pattern to copy for future domains.
"""

import uuid

from sqlmodel import Session

from app import crud
from app.models.items.item import Item
from app.schemas.items.item import ItemCreate


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    return crud.create_item(session=session, item_in=item_in, owner_id=owner_id)
