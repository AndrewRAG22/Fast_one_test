from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_one.schemas import Message, UserDB, UserPublic, UserSchema, UserList

app = FastAPI(title='Minha Api')  # nome da minha api

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        # descompacta o objeto user e passa os campos para o UserDB
        **user.model_dump(),
        id=len(database) + 1,
    )
    database.append(user_with_id)
    return user_with_id

@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}

@app.put('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user: UserSchema, user_id: int):
    breakpoint()