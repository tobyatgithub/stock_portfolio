from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class CompanySearchForm(FlaskForm):
    """
    """
    symbol = StringField('symbol', validators = [DataRequired()])
