from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from api_etl.internal_api.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime.now()) as time:
        new_user = User(username='test', position='tester', email='test@example.com', password='test123')

        session.add(new_user)
        session.commit()
        user = session.scalar(select(User).where(User.username == 'test'))

    user_dict = asdict(user)
    user_dict.pop('id')  # Remove o ID gerado automaticamente

    assert user_dict == {
        'username': 'test',
        'position': 'tester',
        'email': 'test@example.com',
        'password': 'test123',
        'created_at': time,
        'updated_at': time,
    }
