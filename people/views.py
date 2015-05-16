from people import app, db, user_datastore
from flask import render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from people.models.user import User
from people.models.role import Role
from flask.ext.security import Security, SQLAlchemyUserDatastore


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate():
		user = user_datastore.create_user(id = form.username.data, firstName = form.firstName.data, lastName = form.lastName.data, password = form.password.data)
		db.session.commit(user)
		return render_template('index')
	else:
		return render_template('register.html', form=form)

@app.route('/makers')
def makers():
	return render_template('makers.html')

class RegisterForm(Form):
	"""docstring for RegisterForm"""
	firstName = StringField('First Name', validators=[DataRequired()])
	lastName = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Label', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
		

