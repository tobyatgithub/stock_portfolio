from ..src import app
from ..src.models import db
import pytest

@pytest.fixture
# this client gonna hold the server locally
def client():

    def do_nothing():
        pass

    db.session.commit = do_nothing

    yield app.test_client()

    db.session.rollback()


# test the home page
def test_home_route_get():
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to the Stock Portfolio site.</h1>' in rv.data

# home shall forbid post
def test_home_route_post():
    rv = app.test_client().post('/')
    assert rv.status_code == 405

# home shall forbid any delete
def  test_home_route_delete():
    rv = app.test_client().delete('/')
    assert rv.status_code == 405

def test_portfolio_route_get():
    rv = app.test_client().get('/portfolio')
    # import pdb; pdb.set_trace()
    # --> yeah...anything related to rv is not returned
    # ---> yep, use print(), then you can see everything.
    assert rv.status_code == 200
    assert b'<h2>Welcome to the Portfolio</h2>' in rv.data

def test_search_route_get():
    rv = app.test_client().get('/search')
    assert rv.status_code == 200
    assert b'<h2>Search for stocks</h2>' in rv.data

# for any legal post, we will need client
def test_search_porst_pre_redirect(client):
    rv = client.post('/search', data = {'symbol':'sq'}, follow_redirects = False)
    # hum...somehow I'm getting 200 on this...even with follow_redirects = False
    assert rv.status_code == 302

def test_search_post(client):
    rv = client.post('/search', data = {'symbol':'sq'}, follow_redirects = True)
    assert rv.status_code == 200

def test_bunk_symbols(client):
    rv = client.post('/search', data = {'symbol':''}, follow_redirects = True)
    assert rv.status_code == 404 #somehow...this is not 404...

#hum...weird, somehow the routes call client part are not executed.
