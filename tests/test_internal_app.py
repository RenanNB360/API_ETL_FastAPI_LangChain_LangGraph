from fastapi import status


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


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'username': 'alice', 'position': 'tester', 'email': 'alice@example.com'}


def test_read_user_return_not_found(client):
    response = client.get('/users/669')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'alice', 'position': 'tester', 'email': 'alice@example.com'}]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'username': 'bob', 'position': 'tester_master', 'email': 'bob@example.com'}


def test_delete_user_return_not_found(client):
    response = client.delete('/users/669')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
