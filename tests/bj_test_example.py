"""

"""
from flask import g
from ..models import Portfolio
import pytest

class TestBaseRoutes:



    def test_fresh_add_to_portfolio(self, portfolio, authenticated_client):
        assert authenticated_client
        assert en(portPortfolio.query.all()) == 0

        authenticated_client.post(
            '/search',
            data = {'symbol': 'goog'},
            follow_redirects=True)

        rv = authenticated_client.post(
            '/preview',
            data={'symbol': 'goog','companyName': 'Alphabet Inc.','portfolio_id': portfolio.id},
            follow_redirects = True)

        assert rv.status_code == 200

        assert len(portPortfolio.query.all()) == 1
        # register and login
        # post a company

        # check for 200 after redirect
        # redirect to
        # end up with portfolio has the new company
