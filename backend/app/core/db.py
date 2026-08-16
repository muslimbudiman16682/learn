from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models.users.user import User
from app.schemas.users.user import UserCreate

engine = create_engine(str(settings.DATABASE_URL))


# Note: importing app.models.users.user above also runs app/models/__init__.py,
# which imports every domain's table model. Keep that file up to date so
# Alembic and SQLModel.metadata always see every table.
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from app.models import SQLModel
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
