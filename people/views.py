from people import app, db
from flask import render_template, request, redirect, url_for, abort, flash
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from people.models import User
from people.models import Profile
from flask.ext.login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.firstName.data, form.lastName.data, generate_password_hash(form.password.data))
        if user.id is False:
            flash('Username not valid', 'error')
            abort(redirect('register'))
        profile = Profile(form.username.data)
        db.session.add(user)
        db.session.add(profile)
        db.session.commit()
        flash("You've successfully registered. Now login with your credentials.", 'success')
        return redirect(url_for('login'))
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
        user = User.query.get(form.username.data)
        if user is None:
            flash('unknown User', 'error')
            abort(redirect('login'))
        if user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')

        # next = request.args.get('next')
        # if not next_is_valid(next):
        #     return abort(400)
            return redirect(url_for('index'))
        else:
            flash('Username or password wrong', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<username>')
@login_required
def profile(username):
    profile = Profile.query.get(username)
    user = User.query.get(username)
    if user is None:
        abort(404)
    return render_template('profile.html', profile=profile, user=user)


class RegisterForm(Form):
    """docstring for RegisterForm"""
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Label', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
        

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
