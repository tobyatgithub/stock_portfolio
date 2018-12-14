from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.ForeignKey('portfolios.id'), nullable=False)
    name = db.Column(db.String(256), index=True)
    symbol = db.Column(db.String(64), index=True)
    CEO = db.Column(db.String(128))
    # exchange = db.Column(db.String(128))
    # industry = db.Column(db.String(128))
    # website = db.Column(db.String(128))
    # description = db.Column(db.Text)
    # issueType = db.Column(db.String(128))
    # sector = db.Column(db.String(128))

    date_created = db.Column(db.DateTime, default = dt.now())

    def __repr__(self):
        return '<Company {}>'.format(self.name)

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    # foreign key shall be here instead of in user....uhh
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(256), index=True)

    companies = db.relationship('Company', backref='portfolio', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Portfolio {}>'.format(self.name)


class User(db.Model):
    """
    Here we define a class for our portfolio users.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    portfolios = db.relationship('Portfolio', backref='users', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def __init__(self, email, password):
        self.email = email
        self.password = sha256_crypt.encrypt(password) #to encrypt

    @classmethod
    def check_password_hash(cls, user, password):
        """
        takes in user and password, return a boolean value as whether
        the password is correct or not.
        """

        if user:
            if sha256_crypt.verify(password, user.password):
                return True
        return False
