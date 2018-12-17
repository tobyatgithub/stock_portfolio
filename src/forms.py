from flask import render_template, flash, redirect, url_for, session, g, flash
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from .models import Portfolio


class CompanySearchForm(FlaskForm):
    """
    """
    symbol = StringField('symbol', validators=[DataRequired()])


class CompanyAddForm(FlaskForm):
    """
    """
    symbol = StringField('symbol', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    CEO = StringField('CEO', validators=[DataRequired()])
    portfolios = SelectField('portfolios')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios.choices = [(str(c.id), c.name) for c in
        Portfolio.query.filter(Portfolio.user_id == g.user.id).all()]

        # self.portfolios.choices = [(str(c.id), c.name) for c in Portfolio.query.all()]


class PortfolioCreateForm(FlaskForm):
    """
    """
    name = StringField('Portfolio Name', validators=[DataRequired()])


class AuthForm(FlaskForm):
    """
    The form for authorization activities such as register and login in.
    """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
