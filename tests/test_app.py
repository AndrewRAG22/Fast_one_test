from http import HTTPStatus


def test_root_deve_retornar_hello_world(client):
    # Arrange = organizar
    # Act = agir
    response = client.get('/')
    # Assert = afirmar
    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_ola_mundo_em_html(client):
    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


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


def test_listar_usuarios(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'andrew@example.com',
                'username': 'andrew',
            },
        ]
    }


def test_get_user(client):
    # Criar um usuário para poder recuperá-lo
    client.post(
        '/users/',
        json={
            'username': 'andrew',
            'email': 'andrew@example.com',
            'password': 'andrew13',
        },
    )

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'andrew@example.com',
        'username': 'andrew',
    }


def test_atualizar_usuario(client):
    response = client.put(
        '/user/1',
        json={
            'username': 'andrew_updated',
            'email': 'andrew_updated@example.com',
            'password': 'andrew13_updated',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'andrew_updated@example.com',
        'username': 'andrew_updated',
    }


def test_deletar_usuario(client):
    response = client.delete('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'andrew_updated@example.com',
        'username': 'andrew_updated',
    }


def test_usuario_nao_encontrado(client):
    response = client.put(
        '/user/999',
        json={
            'username': 'digdim',
            'email': 'digdim@exemple.com',
            'password': 'digdim13',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}


def test_deletar_usuario_nao_encontrado(client):
    response = client.delete('/user/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}


def test_listar_usuario_nao_encontrado(client):
    response = client.get('/users/997')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nao achei'}
