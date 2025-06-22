# import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_etl.internal_api.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


"""db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
if db_user:
    if db_user.username == user.username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = 'Username already exists'
        )
    elif db_user.email == user.email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = 'Email already exists'
        )

db_user = User(
    username = user.username,
    position = user.position,
    email = user.email,
    password = user.password
)

session.add(db_user)
session.commit()
session.refresh(db_user)

return db_user"""
