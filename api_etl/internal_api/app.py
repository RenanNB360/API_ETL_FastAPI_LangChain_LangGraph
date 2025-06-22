from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api_etl.internal_api.database import get_session
from api_etl.internal_api.models import User
from api_etl.internal_api.schemas import Message, Token, UserList, UserPublic, UserSchema
from api_etl.internal_api.security import get_password_hash, verify_password

app = FastAPI()

database = []


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')

    db_user = User(
        username=user.username, position=user.position, email=user.email, password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    return user_db


@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(offset: int = 0, limit: int = 10, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
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


@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    session.delete(user_db)
    session.commit()

    return Message(message='User deleted!')


@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
