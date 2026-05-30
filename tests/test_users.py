from http import HTTPStatus

from fast_one.schemas import UserPublic


def test_listar_usuarios_com_usuario(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_criar_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'andrew',
            'email': 'andrew@example.com',
            'password': 'andrew13',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'andrew@example.com',
        'username': 'andrew',
    }


def test_atualizar_usuario(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'andrew_updated',
            'email': 'andrew_updated@example.com',
            'password': 'andrew13_updated',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'email': 'andrew_updated@example.com',
        'username': 'andrew_updated',
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bimbo@example.com',
            'password': 'minhasenha',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username ou email já existe'}


def test_deletar_usuario(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuario deletado'}


def test_usuario_nao_encontrado(client, token):
    response = client.put(
        '/users/50',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'digdim',
            'email': 'digdim@exemple.com',
            'password': 'digdim13',
        },
    )

    print('\nERRO DO FASTAPI:', response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}


def test_deletar_usuario_nao_encontrado(client, token):
    response = client.delete(
        '/users/60',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}


def test_listar_usuario_nao_encontrado(client, token):
    response = client.get(
        '/users/997', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}


def test_create_user_should_return_409_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username já existe'}


def test_create_user_should_return_409_email_exists__exercicio(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email já existe'}


def test_get_user___exercicio(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'boob',
            'email': 'boib@example.com',
            'password': 'myinewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
