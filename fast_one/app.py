from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_one.database import get_session
from fast_one.models import User
from fast_one.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Minha Api')  # nome da minha api


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


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(
    user_id: int,
    session=Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nao achei'
        )
    return db_user


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(  # escreve uma msg para o erro
                detail='Username já existe', status_code=HTTPStatus.CONFLICT
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email já existe'
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)  # adiciona usuario ao banco de dados
    session.commit()  # salva as alteracoes no banco de dados
    session.refresh(db_user)  # atualiza o objeto db_user

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user: UserSchema, user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nao achei'
        )
    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou email já existe',
        )


@app.delete(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nao achei'
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'Usuario deletado'}
