from http import HTTPStatus
from sqlalchemy import create_engine, select
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title=' Meu projeto API')
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    
    engine = create_engine(Settings().DATABASE_URL)

    session = Session(engine)

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) |( User.email == user.email)                                               
            )
    )
    # Se der um erro : 
    # ele retornara ou User ou None, assim, se existir, 
    # a condição acima de um ou outro, ele deve retornar um erro

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

    # Se não der um erro : 
    #def get_session():
    #    with Session(engine) as session:
    #        yield session

    #user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    #database.append(user_with_id)

    #return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_user():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
