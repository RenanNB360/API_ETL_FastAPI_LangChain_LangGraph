from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from api_etl.internal_api.access_control.security import get_password_hash
from api_etl.internal_api.access_control.settings import Settings
from api_etl.internal_api.app import app
from api_etl.internal_api.utils.database import get_session
from api_etl.internal_api.utils.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///database.db', connect_args={'check_same_thread': False}, poolclass=StaticPool
    )
    # table_registry.metadata.create_all(engine)

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)

    """async with AsyncSession(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)"""


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 6, 21)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: AsyncSession):
    password = 'test123'
    user = User(username='test', position='Tester', email='test@example.com', password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})

    return response.json()['access_token']


@pytest.fixture
def admin_user(session):
    user = User(
        username='admin', position='administrator', email='admin@example.com', password=get_password_hash('admin123')
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post('/auth/token', data={'username': admin_user.username, 'password': 'admin123'})
    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
