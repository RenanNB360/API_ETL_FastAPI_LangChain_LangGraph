from fastapi import FastAPI, status

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


@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users():
    return {'users': database}
