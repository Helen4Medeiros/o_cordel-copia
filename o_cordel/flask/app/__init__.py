from flask import Flask
from config import Config
from flask_login import LoginManager
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

myApp = Flask(__name__)
myApp.config.from_object(Config)
myApp.jinja_env.finalize = lambda x: x if x is not None else '' # para que templates não exibam None
login_manager = LoginManager(myApp)
login_manager.login_view = 'login' # Define a página de login
sql_engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

from app import routes, models, dao
