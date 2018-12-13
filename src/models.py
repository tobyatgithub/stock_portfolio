from flask_sqlalchemy import SQLAlchemy
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
    name = db.Column(db.String(256), index=True)

    companies = db.relationship('Company', backref='portfolio', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Portfolio {}>'.format(self.name)
