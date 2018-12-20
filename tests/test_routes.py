# ### we dont' need these import because we have defined another one in conftest.py
# # from ..src import app
# # from ..src.models import db


# import pytest
# from flask import g


# # from ..src.auth import load_logged_in_user
# ### we dont' need this client because we have defined another one in conftest.py
# # @pytest.fixture
# # # this client gonna hold the server locally
# # def client():

# #     def do_nothing():
# #         pass

# #     db.session.commit = do_nothing

# #     yield app.test_client()

# #     db.session.rollback()



# # test the home page
# def test_home_route_get(app):
#     rv = app.test_client().get('/')
#     assert rv.status_code == 200
#     assert b'<h1>Welcome to the Stock Portfolio site.</h1>' in rv.data

# # home shall forbid post
# def test_home_route_post(app):
#     rv = app.test_client().post('/')
#     assert rv.status_code == 405

# # home shall forbid any delete
# def  test_home_route_delete(app):
#     rv = app.test_client().delete('/')
#     assert rv.status_code == 405

# def test_portfolio_route_get(app):
#     rv = app.test_client().get('/portfolio')
#     # --> yeah...anything related to rv is not returned
#     # ---> yep, use print(), then you can see everything.
#     # 12/13/18 now we don't allow access to portfolio without login,
#     # any not-autorized will be redirected
#     assert rv.status_code == 302
#     # assert b'<h2>Welcome to your Portfolio</h2>' in rv.data

# def test_search_route_get(app):
#     rv = app.test_client().get('/search')
#     # import pdb; pdb.set_trace()
#     assert rv.status_code == 302
#     # assert b'<h3>Please create a Category' in rv.data
#     # assert b'<h2>Search for stocks</h2>' in rv.data

# # for any legal post, we will need client
# def test_search_porst_pre_redirect(app):
#     rv = app.test_client().post('/search',
#         data = {'symbol':'sq'},
#         follow_redirects = False)
#     # hum...somehow I'm getting 200 on this...even with follow_redirects = False
#     assert rv.status_code == 302

# def test_search_post(app):
#     rv = app.test_client().post(
#         '/search',
#         data = {'symbol':'sq'},
#         follow_redirects = True
#         )
#     # if follow redirect, will be lead to login page with a 200 status code
#     assert rv.status_code == 200

# # # no longer return 404 for empty search
# # def test_bunk_symbols(app):
# #     rv = app.test_client().post(
# #         '/search',
# #         data = {'symbol':''},
# #         follow_redirects = True)
# #     assert rv.status_code == 302

# #hum...weird, somehow the routes call client part are not executed.


# # SUPPORT function for login test
# def login(app, email, password):
#     return app.test_client().post(
#         '/login',
#         data=dict(
#             email=email,
#             password=password
#         ),
#         follow_redirects=True)

# # def logout(app):
# #     return app.client.get('/logout', follow_redirects=True)

# def test_login1(app):
#     rv = login(app, 'baduser', 'badpassword')
#     # import pdb; pdb.set_trace()
#     assert b'Invalid emial or password.' in rv.data


# def test_login2(app):
#     rv = login(app, 'test_user1', '1234')
#     # import pdb; pdb.set_trace()
#     assert b'<h3>Welcome to the site test_user1</h3>' in rv.data

# # Now I kind of see why we have to use a class for this.
# # so far I didn't find any method to pass along this logged-in status
# # for any /search action. Find one suggestion on stackoverflow
# # where this problem seems is solved by passing along the app.post
# # result into self
# # ref: https://stackoverflow.com/questions/28142751/test-a-login-required-flask-application

# # def test_login_and_search(app):
# #     assert login(app, 'test_user1', '1234').status_code == 200
# #     # load_logged_in_user()
# #     import pdb; pdb.set_trace()
# #     rv = app.test_client().post('/search',
# #         data = {'symbol' : 'V'})
# #     print('dasbda')
# #     assert True
# # def test_register1(app):
# #     rv = login(app, 'user1', '1234')
# #     # assert b'Invalid emial or password.' in rv.data
