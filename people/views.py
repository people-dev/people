from people import app, db, mail
from flask import render_template, request, redirect, url_for, abort, flash
from flask.ext.uploads import UploadSet, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, DecimalField 
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, IntegerRangeField
from wtforms.widgets import TextArea
from people.models import User
from people.models import Profile
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug import secure_filename
from flask_mail import Message
import time
import datetime

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        timeStamp = time.time()
        user = User(form.username.data, form.firstName.data, form.lastName.data, generate_password_hash(form.password.data), timeStamp)
        if user.id is False:
            flash('Username not valid', 'error')
            abort(redirect('register'))
        profile = Profile(form.username.data)
        db.session.add(user)
        db.session.add(profile)
        db.session.commit()
        # msg = Message('People Confirm account', recipients=['3deinert@informatik.uni-hamburg.de'], html='Your account has been successfully created and this is the confirmation mail')
        # mail.send(msg)
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
            flash('Unknown User', 'error')
            abort(redirect('login'))
        if user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')

        # next = request.args.get('next')
        # if not next_is_valid(next):
        #     return abort(400)
            return redirect(url_for('profile', username=current_user.id))
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
    if user is None or profile is None:
        abort(404)

    user.created_at = datetime.datetime.fromtimestamp(user.created_at).strftime('%Y-%m-%d')
    if profile.updated_at is not None:
        profile.updated_at = datetime.datetime.fromtimestamp(profile.updated_at).strftime('%Y-%m-%d %H:%M')
    return render_template('profile.html', profile=profile, user=user)


@app.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def editProfile(username):
    if current_user.id == username:
        form = EditProfileForm()
        if request.method == 'POST':
        # if form.validate_on_submit():
            timeStamp = time.time()
            profile = Profile.query.get(username)
            profile.name=form.name.data
            profile.gender=form.gender.data
            profile.major=form.major.data
            profile.semester=form.semester.data
            profile.phone=form.phone.data
            profile.mobile=form.mobile.data
            profile.jabber=form.jabber.data
            profile.updated_at = timeStamp
            profile.about = form.about.data
            if form.picture.data.filename is not '':
                filename = secure_filename(form.picture.data.filename)
                form.picture.data.save('people'+url_for('static',filename='images/'+filename))
                profile.image = filename
            db.session.commit()
            return redirect(url_for('profile', username=current_user.id))
        profile = Profile.query.get(username)
        user = User.query.get(username)
        form.about.data = profile.about
        if user is None or profile is None:
            abort(404)
        filename = None
        return render_template('editProfile.html', profile=profile, user=user, form=form, filename=filename)
    else:
        abort(403)

class RegisterForm(Form):
    """docstring for RegisterForm"""
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Label', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
        

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditProfileForm(Form):
    name = StringField('Name')
    gender = StringField('Gender')
    birthday = DateField('Birthday', format='%d-%m-%Y')
    selectMajors = [('Bsc. Inf', 'Bsc. Inf'), ('Bsc. CIS', 'Bsc. CIS'), ('Bsc. SSE', 'Bsc. SSE'), ('Bsc. MCI', 'Bsc. MCI'), ('Bsc. WiInf', 'Bsc. WiInf')]
    major = SelectField('Major', choices = selectMajors)
    semester = StringField('Semester')
    phone = StringField('Phone')
    mobile = StringField('Mobile')
    jabber = StringField('Jabber')
    about =  StringField('About you', widget=TextArea())
    images = UploadSet('images', IMAGES)
    picture = FileField('Profile Picture', validators=[FileAllowed(images, 'Images only!')])


