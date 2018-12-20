import pytest
from flask import g
from ..src import app
# from flaskr.db import get_db

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthActions(client)


def test_register(client, app):
    assert client.get('/login').status_code == 200
    # response = client.post(
    #     '/login', data={'username': 'a', 'password': 'a'}
    # )
    response = client.post(
        '/login', data={'username': 'test_user1', 'password': '1234'}
    )
    import pdb; pdb.set_trace()

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None
