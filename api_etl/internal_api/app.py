from fastapi import FastAPI, status

from api_etl.internal_api.routers import auth, users
from api_etl.internal_api.utils.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
