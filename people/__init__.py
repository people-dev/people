from flask import Flask

SECRET_KEY = "foobar"

app = Flask(__name__)
app.config.from_object(__name__)


import people.views
