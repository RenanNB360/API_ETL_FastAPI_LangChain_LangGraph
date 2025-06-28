from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_etl.internal_api.access_control.security import (
    create_access_token,
    verify_password,
)
from api_etl.internal_api.utils.database import get_session
from api_etl.internal_api.utils.models import User
from api_etl.internal_api.utils.schemas import Token

router = APIRouter(prefix='/auth', tags=['authentication users'])

Auth2Password = Annotated[OAuth2PasswordRequestForm, Depends()]
Sessiondb = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: Auth2Password, session: Sessiondb):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
