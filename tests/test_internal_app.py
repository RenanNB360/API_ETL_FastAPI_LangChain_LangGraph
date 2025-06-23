from fastapi import status

from api_etl.internal_api.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'alice', 'position': 'tester', 'password': 'alice123', 'email': 'alice@example.com'},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'id': 1, 'username': 'alice', 'position': 'tester', 'email': 'alice@example.com'}


def test_create_username_exists_error(client, user):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
    )

    response_update = client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester2', 'email': 'fausto2@example.com', 'password': 'fausto2123'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Username already exists'}


def test_create_email_exists_error(client, user):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
    )

    response_update = client.post(
        '/users/',
        json={'username': 'fausto2', 'position': 'tester2', 'email': 'fausto@example.com', 'password': 'fausto2123'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Email already exists'}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_schema


def test_read_user_return_not_found(client):
    response = client.get('/users/669')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_read_users(client, token):
    response = client.get('/users/', headers=...)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={'username': 'bob', 'position': 'tester_master', 'email': 'bob@example.com', 'password': 'bob123'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'username': 'bob', 'position': 'tester_master', 'email': 'bob@example.com'}


def test_update_user_return_not_found(client):
    response = client.put(
        '/users/669',
        json={'username': 'bob', 'position': 'tester_master', 'email': 'bob@example.com', 'password': 'bob123'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
    )

    response_update = client.put(
        f'/users/{user.id}',
        json={'username': 'fausto', 'position': 'tester', 'email': 'bob@example.com', 'password': 'bob123'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_return_not_found(client):
    response = client.delete('/users/669')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_get_token(client, user):
    response = client.post('/token', data={'username': user.username, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
