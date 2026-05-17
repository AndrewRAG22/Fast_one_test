from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_one.app import app


def test_root_deve_retornar_hello_world():
    # Arrange = organizar
    client = TestClient(app)
    # Act = agir
    response = client.get('/')
    # Assert = afirmar
    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_ola_mundo_em_html():
    client = TestClient(app)

    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text
