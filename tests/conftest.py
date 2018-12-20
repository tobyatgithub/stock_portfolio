from ..src.models import Company, Portfolio
from ..src.models import db as _db
from ..src import app as _app
import pytest
import os

@pytest.fixture()
def app(request):
    """
    session-wide testable flask application
    """
    _app.config.from_mapping(
        TESTING = True,
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,
    )

    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):
    """
    Session-wide test database
    """

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    """
    creates a new database session for testing
    """
    # initalize talking between db
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind = connection, binds = {})
    session = db.create_scoped_session(option = options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    # request.addfinalizer(teardown)
    return session


@pytest.fixture()
def client(app, db, session):
    """
    """
    # we need db and session for the following code to happen
    # so...even we are not calling db or session in word, but
    # we do need them to make this work.
    client = app.test_client()
    ctx = app.app_context()

    # you have to have db and session for ctx.push to make current into the environment
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def authenticated_client(client, user):
    """
    """
    client.post(
        '/login',
        data={'email':user.email, 'password':'1234'}, # we hard code password bcz user.password is hashed.
        follow_redirects=True,
    )
    yield client # use yield instead of return, as yield will not change any content. yiled ~= temparaily return

    # and after yield finished, you usually will have some cleaning work afterward
    client.get('/logout')


@pytest.fixture()
def user(session):
    """
    """
    user = User(email = 'test_user1', password = '1234')

    session.add(user)
    session.commit()
    return user


@pytest.fixture()
def portfolio(session, user):
    """
    """
    portfolio = Portfolio(name='Default')

    session.add(portfolio)
    session.commit()
    return portfolio

# @pytest.fixture()
# def company(session, portfolio):
#     """
#     """
#     company = Company(name='Apple Inc.', symbol = 'AAPL', portfolio_id=portfolio.id)
