from fastapi import status

from api_etl.internal_api.utils.schemas import UserPublic


def test_create_user(client, admin_token):
    response = client.post(
        '/users/',
        json={'username': 'alice', 'position': 'administrator', 'password': 'alice123', 'email': 'alice@example.com'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert str(response.json()['id']) == '2'
    assert response.json()['username'] == 'alice'
    assert response.json()['position'] == 'administrator'
    assert response.json()['email'] == 'alice@example.com'


def test_create_username_exists_error(client, admin_token):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    response_update = client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester2', 'email': 'fausto2@example.com', 'password': 'fausto2123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Username already exists'}


def test_create_email_exists_error(client, admin_token):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    response_update = client.post(
        '/users/',
        json={'username': 'fausto2', 'position': 'tester2', 'email': 'fausto@example.com', 'password': 'fausto2123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Email already exists'}


def test_regular_user_cant_create_users(client, token):
    response = client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Admin privileges required'}


def test_jwt_invalid_token_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'alice', 'position': 'administrator', 'password': 'alice123', 'email': 'alice@example.com'},
        headers={'Authorization': 'Bearer token-invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_schema


def test_read_user_return_not_found(client, token):
    response = client.get('/users/669', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_jwt_invalid_token_read_user(client):
    response = client.get('/users/1', headers={'Authorization': 'Bearer token-invalid'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': [user_schema]}


def test_jwt_invalid_token_read_users(client):
    response = client.get('/users/', headers={'Authorization': 'Bearer token-invalid'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_update_user(client, admin_token):
    response = client.put(
        '/users/1',
        json={'username': 'bob', 'position': 'administrator', 'email': 'bob@example.com', 'password': 'bob123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert str(response.json()['id']) == '1'
    assert response.json()['username'] == 'bob'
    assert response.json()['position'] == 'administrator'
    assert response.json()['email'] == 'bob@example.com'


def test_update_user_return_not_found(client, admin_token):
    response = client.put(
        '/users/669',
        json={'username': 'bob', 'position': 'tester_master', 'email': 'bob@example.com', 'password': 'bob123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_integrity_error(client, admin_token, admin_user):
    client.post(
        '/users/',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    response_update = client.put(
        f'/users/{admin_user.id}',
        json={'username': 'fausto', 'position': 'tester', 'email': 'bob@example.com', 'password': 'bob123'},
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response_update.status_code == status.HTTP_409_CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}


def test_regular_user_cant_update_users(client, token):
    response = client.put(
        '/users/1',
        json={'username': 'fausto', 'position': 'tester', 'email': 'fausto@example.com', 'password': 'fausto123'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_invalid_token_update_user(client):
    response = client.put(
        '/users/1',
        json={'username': 'alice', 'position': 'administrator', 'password': 'alice123', 'email': 'alice@example.com'},
        headers={'Authorization': 'Bearer token-invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user(client, admin_token):
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {admin_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_return_not_found(client, admin_token):
    response = client.delete('/users/669', headers={'Authorization': f'Bearer {admin_token}'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_regular_user_cant_delete_users(client, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_invalid_token_delete_user(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
