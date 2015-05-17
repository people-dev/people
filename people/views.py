from people import app, db 
from flask import render_template, request, redirect, url_for, abort, flash
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from people.models.user import User
from flask.ext.login import login_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate():
		user = User(form.username.data, form.firstName.data, form.lastName.data, generate_password_hash(form.password.data))
		db.session.add(user)
		db.session.commit()
		return render_template('index.html')
	else:
		return render_template('register.html', form=form)

@app.route('/makers')
def makers():
	return render_template('makers.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        login_user(user)

        flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not next_is_valid(next):
            return abort(400)

        return redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form)


class RegisterForm(Form):
	"""docstring for RegisterForm"""
	firstName = StringField('First Name', validators=[DataRequired()])
	lastName = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Label', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
		

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])