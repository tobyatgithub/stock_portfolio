# Flask - wtf Forms...
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class StockSearchForm(FlaskForm):
    """
    Form inherit from flaskform to return results of stock search.
    """

    stock_name = StringField('Stock Name', validators=[DataRequired()])
