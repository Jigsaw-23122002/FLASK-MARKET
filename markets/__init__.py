from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
app.config['SECRET_KEY']='2f8a6f92623d8a218b15ecf6'

db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view="login"

from markets import routes