from dataclasses import asdict

from sqlalchemy import select

from api_etl.internal_api.models import User


def test_create_user(session):
    new_user = User(username='test', position='tester', email='test@example.com', password='test123')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))
    assert asdict(user) == {
        'username': 'test',
        'position': 'tester',
        'email': 'test@example.com',
        'password': 'test123',
        'created_at': ...,
    }
