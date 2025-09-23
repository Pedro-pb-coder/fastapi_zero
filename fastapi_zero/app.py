from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.schemas import Message, UserDB, UserPublic, UserSchema

app = FastAPI(title=' Meu projeto API')
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1
    )
    database.append(user_with_id)
    return user_with_id
