from flask import Flask
import os

# get root of the project. The benefit is path is not hard coded and shall be adaptable.
basedir = os.path.abspath(os.path.dirname(__file__))

# create app
app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config= True # allows config to be in the flask app
)

DATABASE_URL = os.environ.get('DATABASE_URL')

if os.environ.get('TESTING') == 'True':
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL')


app.config.from_mapping(
    SECRET_KEY = os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = DATABASE_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

# mont config from source directory
from . import routes, forms, models, exceptions
