from dataclasses import asdict
from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_etl.internal_api.utils.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User, time=datetime.now()) as time:
        new_user = User(username='test', position='tester', email='test@example.com', password='test123')

        session.add(new_user)
        await session.commit()
        user = await session.scalar(select(User).where(User.username == 'test'))

    user_dict = asdict(user)
    user_dict.pop('id')

    assert user_dict == {
        'username': 'test',
        'position': 'tester',
        'email': 'test@example.com',
        'password': 'test123',
        'created_at': time,
        'updated_at': time,
    }
