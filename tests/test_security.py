import pytest
from fastapi import HTTPException, status
from jwt import decode, encode

from api_etl.internal_api.security import ALGORITHM, SECRET_KEY, create_access_token, get_current_user


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_get_current_user_missing_subject_email(session):
    invalid_token = encode({}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session=session, token=invalid_token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'


def test_get_current_user_not_found(session):
    valid_token = encode({'sub': 'nao_existe@example.com'}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session=session, token=valid_token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'
