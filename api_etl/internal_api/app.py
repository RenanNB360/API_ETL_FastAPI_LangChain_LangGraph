from fastapi import FastAPI, HTTPException, status

from api_etl.internal_api.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')
    return database[user_id - 1]


@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')
    return database.pop(user_id - 1)
