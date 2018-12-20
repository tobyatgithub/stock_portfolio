

class TestCompanyModel:
    """
    """
    def test_create_company(self, company):
        """
        """
        assert company.id > 0

    def test_company_name(self, company):
        """
        """
        assert company.name == 'Microsoft'

    def test_company_symbol(self, company):
        """
        """
        assert company.symbol == 'msft'

    def test_company_portfolio_id(self, company):
        """
        """
        assert company.portfolio_id > 0


class TestPortfolioModel:
    """
    """
    def test_create_portfolio(self, portfolio):
        """
        """
        assert portfolio.id > 0

    def test_portfolio_name(self, portfolio):
        """
        """
        assert portfolio.name is not None

    def test_portfolio_user_id(self, portfolio):
        """
        """
        assert portfolio.user_id > 0


class TestUserModel:
    """
    """
    def test_user_create(self, user):
        """
        """
        assert user.id > 0

    def test_user_email(self, user):
        """
        """
        assert user.email == 'test_user1'

    def test_user_check_password(self, user):
        """
        """
        from ..src.models import User
        assert User.check_password_hash(user, '1234')


