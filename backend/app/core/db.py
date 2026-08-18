from sqlmodel import Session, create_engine, select, SQLModel

from app import crud
from app.core.config import settings
from app.models.auths.user import User
from app.schemas.auths.user import UserCreate

engine = create_engine(str(settings.DATABASE_URL))

# Monkeypatch SQLAlchemy UUID bind processor to accept string UUIDs (coerce to uuid.UUID)
import sqlalchemy
import uuid as _uuid

def _patch_uuid_type(uuid_type):
    # patch bind_processor to accept str by coercing to uuid.UUID
    _orig_bind = getattr(uuid_type, "bind_processor", None)

    def _bind_processor(self, dialect):
        orig = _orig_bind(self, dialect) if _orig_bind else None

        if orig is None:
            return None

        def process(value):
            if isinstance(value, str):
                try:
                    value = _uuid.UUID(value)
                except Exception:
                    pass
            return orig(value)

        return process

    uuid_type.bind_processor = _bind_processor

try:
    # try both common names used by SQLAlchemy (UUID and Uuid)
    if hasattr(sqlalchemy.sql.sqltypes, "UUID"):
        _patch_uuid_type(sqlalchemy.sql.sqltypes.UUID)
    if hasattr(sqlalchemy.sql.sqltypes, "Uuid"):
        _patch_uuid_type(sqlalchemy.sql.sqltypes.Uuid)
except Exception:
    # if SQLAlchemy's UUID type isn't available, skip monkeypatch
    pass


# Note: importing app.models.users.user above also runs app/models/__init__.py,
# which imports every domain's table model. Keep that file up to date so
# Alembic and SQLModel.metadata always see every table.
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Ensure tables exist for tests and local runs when Alembic isn't used
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.create_user(session=session, user_create=user_in)
        # grant superuser after creation
        user.is_superuser = True
        session.add(user)
        session.commit()
        session.refresh(user)
