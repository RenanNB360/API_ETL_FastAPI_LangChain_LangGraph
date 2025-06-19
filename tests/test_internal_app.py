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
