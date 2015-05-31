from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile("../config.py")

mail = Mail(app)

db = SQLAlchemy(app)

import people.login
import people.views
