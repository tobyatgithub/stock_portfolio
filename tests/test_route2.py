from flask import g
from ..src.models import Portfolio


class TestFixtures:
    """
    """
    def test_authenticated_client(self, authenticated_client):
        """Confirm authenticated_client fixture ok
        """
        assert authenticated_client

    def test_portfolio_fixture(self, portfolio, user):
        """Confirm portfolio fixture works as expected
        """
        # portfolio should be added to db
        assert Portfolio.query.first().id == portfolio.id

        # portfolio's user should match
        assert portfolio.user_id == user.id

        # portfolio should start with no companies
        assert not Portfolio.query.first().companies

    def test_add_fresh_company_to_portfolio(self, authenticated_client, portfolio):
        """Add a 'fresh' company aka one not already in portfolio
        """
        # need to first post from search page in order to add company stock symbol to session
        authenticated_client.post('/search', data={'symbol': 'goog'}, follow_redirects=True)

        # simulate form input DANGER: make sure form keys match or else validation will fail!
        form_data = {'symbol': 'goog', 'name': 'Alphabet Inc.', 'CEO': 'Larry Page', 'portfolios': portfolio.id}

        # post the form data but do not follow redirects
        rv = authenticated_client.post('/preview', data=form_data, follow_redirects=False)
        # confirm that company added to portfolio
        assert len(Portfolio.query.first().companies) == 1

        # confirm redirect
        assert rv.status_code == 302

    def test_add_fresh_company_to_portfolio_redirect(self, authenticated_client, portfolio):
        """Add a fresh company and follow redirect
        """

        # need to first post from search page in order to add company stock symbol to session
        authenticated_client.post('/search', data={'symbol': 'goog'}, follow_redirects=True)

        # simulate form input
        form_data = {'symbol': 'goog', 'companyName': 'Alphabet Inc.', 'CEO': 'Larry Page', 'portfolios': portfolio.id}

        # post the form data and follow redirect
        rv = authenticated_client.post('/preview', data=form_data, follow_redirects=True)

        # confirm status
        assert rv.status_code == 200

        # confirm proper markup
        assert b'<h2>Welcome to your Portfolio</h2>' in rv.data


class TestBaseRoutes:
    """
    """
    def test_home_route_status(self, client):
        """
        """
        res = client.get('/')
        assert res.status_code == 200

    def test_home_route_body(self, client):
        """
        """
        res = client.get('/')
        assert b'<h1>Welcome to the Stock Portfolio site.</h1>' in res.data

    def test_unknown_route_status(self, client):
        """
        """
        res = client.get('/does_not_exist')
        assert res.status_code == 404


class TestAuthentication:
    """
    """
    def test_registration_page_status(self, client):
        """
        """
        res = client.get('/register')
        assert res.status_code == 200

    def test_registration_body(self, client):
        """
        """
        res = client.get('/register')
        assert b'Register' in res.data

    def test_registration_redirect_status(self, client):
        """
        """
        res = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert res.status_code == 200

    def test_registration_redirect_to_login(self, client):
        """
        """
        res = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert b'Registration compelte. Please Log in.' in res.data

    def test_registered_user_can_login(self, client):
        """
        """
        client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        res = client.post(
            '/login',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert res.status_code == 200
        assert b'Welcome to your Portfolio' in res.data
        assert b'<h3>Create a new Portfolio!</h3>' in res.data

    def test_register_invalid_inputs(self, client):
        """
        """
        res = client.post(
            '/register',
            follow_redirects=True,
        )
        assert b'Register' in res.data

    def test_login_page_status(self, client):
        """
        """
        res = client.get('/login')
        assert res.status_code == 200

    def test_login_page_res_body(self, client):
        """
        """
        res = client.get('/login')
        assert b'<h2>Login:</h2>' in res.data

    def test_login_page_redirect_status(self, client, user):
        """
        """
        res = client.post(
            '/login',
            data={'email': user.email, 'password': 'secret'},
            follow_redirects=True,
        )
        assert res.status_code == 200

    def test_login_page_redirect_to_portfolio_detail(self, client, user, company):
        """
        """
        res = client.post(
            '/login',
            data={'email': user.email, 'password': '1234'},
            follow_redirects=True,
        )
        expected = f'{company.name}'
        assert expected.encode() in res.data

    def test_login_invalid_inputs(self, client):
        """
        """
        res = client.post(
            '/login',
            follow_redirects=True,
        )
        assert b'<h2>Login:</h2>' in res.data

    def test_logout_redirect_status(self, authenticated_client):
        """
        """
        res = authenticated_client.get('/logout', follow_redirects=True)
        assert res.status_code == 200

    def test_login_page_session(self, authenticated_client, flask_session):
        """
        """
        assert g.user is not None

        assert flask_session.get('user_id') == g.user.id

    def test_logout_unauthenticated(self, client, flask_session):
        """
        """
        client.get('/logout')

        assert flask_session.get('user_id') is None


class TestAuthenticatedRoutes:
    """

    """
    def test_search_route_status(self, authenticated_client):
        """
        """
        res = authenticated_client.get('/search')
        assert res.status_code == 200

    def test_search_route_status_unauthenticated(self, client):
        """
        """
        res = client.get('/search', follow_redirects=True)
        assert res.status_code == 200
        # import pdb; pdb.set_trace()
        assert b'<h2>Login:</h2>' in res.data

    def test_portfolio_route_no_companies(self, authenticated_client):
        """
        """
        res = authenticated_client.get('/portfolio')
        assert b'<h3>Create a new Portfolio!</h3>' in res.data

    def test_protected_route_with_user_fixture(self, client, user):
        """
        Using the user fixture's id
        add it to the current session.
        This should trigger the auth to load user with the given user_id
        add store it in 'g'
        after that protected routes should be reachable
        """

        # set session's user_id
        with client.session_transaction() as flask_session:
            flask_session['user_id'] = user.id

        # navigate to protected route
        rv = client.get('/search')

        # auth module's @app.before_request should result in
        # g.user being set
        assert g.user == user

        # good login gives 200
        assert rv.status_code == 200
