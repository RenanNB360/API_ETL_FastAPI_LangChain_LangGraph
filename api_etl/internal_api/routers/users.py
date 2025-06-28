from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api_etl.internal_api.access_control.security import (
    get_admin_user,
    get_current_user,
    get_password_hash,
)
from api_etl.internal_api.utils.database import get_session
from api_etl.internal_api.utils.models import User
from api_etl.internal_api.utils.schemas import FilterPage, Message, UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['handle users'])

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(get_admin_user)]


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: SessionDep, current_user: AdminUserDep):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')

    db_user = User(
        username=user.username,
        position=user.position,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user(user_id: int, session: SessionDep, current_user: CurrentUserDep):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    return user_db


@router.get('/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(session: SessionDep, current_user: CurrentUserDep, filter_users: Annotated[FilterPage, Query()]):
    users = session.scalars(select(User).limit(filter_users.limit).offset(filter_users.offset))
    return {'users': users}


@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: SessionDep, current_user: AdminUserDep):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.position = user.position
        user_db.password = get_password_hash(user.password)

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username or Email already exists')


@router.delete('/{user_id}', status_code=status.HTTP_200_OK, response_model=Message)
def delete_user(user_id: int, session: SessionDep, current_user: AdminUserDep):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    session.delete(user_db)
    session.commit()

    return Message(message='User deleted!')
