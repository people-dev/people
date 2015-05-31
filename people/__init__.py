from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_pyfile("../config.py")

mail = Mail(app)
timedSerializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

db = SQLAlchemy(app)

import people.login
import people.views
