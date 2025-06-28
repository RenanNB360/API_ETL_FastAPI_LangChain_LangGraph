# import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_etl.internal_api.access_control.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
