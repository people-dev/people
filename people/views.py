from people import app
from flask import render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
	form = RegisterForm()
	return render_template('register.html', form=form)


class RegisterForm(Form):
	"""docstring for RegisterForm"""
	firstName = StringField('First Name', validators=[DataRequired()])
	lastName = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Label', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
		