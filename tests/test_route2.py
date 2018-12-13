class TestClass:
    """
    here're the scopes. set up to build db, app, and sessions for each
    test that runs.

    Interesting here is, we can define app, db, sessions in conftest.py,
    and we don't need to import it here And can just use them, Pytest
    does the work.

    This is a common way people do test cases.


    """

    # these two classmethods are not really required here.
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
