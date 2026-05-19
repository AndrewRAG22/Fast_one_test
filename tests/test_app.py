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