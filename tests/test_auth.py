from fastapi import status


def test_get_token(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_invalid_username(client):
    response = client.post('/auth/token', data={'username': 'nao_existe', 'password': 'qualquer_senha'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_invalid_password(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': 'senha_incorreta'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
