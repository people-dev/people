from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin

app = Flask(__name__)
app.config.from_pyfile("../config.py")

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

from people.models.user import User
from people.models.role import Role



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


import people.views
