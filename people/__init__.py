from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager



app = Flask(__name__)
app.config.from_pyfile("../config.py")

db = SQLAlchemy(app)
login_manager = LoginManager()


login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


import people.views
