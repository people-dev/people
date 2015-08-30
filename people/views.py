from people import app, db, mail, timedSerializer
from flask import render_template, request, redirect, url_for, abort, flash, g
from flask.ext.uploads import UploadSet, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, DecimalField, HiddenField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, IntegerRangeField
from wtforms.widgets import TextArea
from people.models import User
from people.models import Notification
from people.models import Request
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug import secure_filename
from flask_mail import Message
import time
import datetime

@app.before_request
def before_request():
    if not current_user.is_anonymous():
        g.notifications = Notification.query.filter_by(to_user=current_user) 
        for notification in g.notifications:
            if type(notification.created_at) is not str:
                # temp fix for notification time being converted again on POST from e.g. editProfile 
                notification.created_at = datetime.datetime.fromtimestamp(notification.created_at).strftime('%Y-%m-%d')


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
        db.session.add(user)
        db.session.commit()
        # msg = Message('People Confirm account', recipients=['3deinert@informatik.uni-hamburg.de'], html='Your account has been successfully created and this is the confirmation mail')
        # mail.send(msg)
        print(user.email)
        token = timedSerializer.dumps(user.email, salt='email-confirm-key')
        print(url_for('confirm_email', token=token, _external=True))
        flash("You've successfully registered. Check your emails to confirm your account.", 'success')
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
            if user.is_active():
                login_user(user)
                flash('Logged in successfully.', 'success')
            else:
                flash('User not activated', 'error')
                return redirect(url_for('login'))

        # next = request.args.get('next')
        # if not next_is_valid(next):
        #     return abort(400)
            return redirect(url_for('profile', id=current_user.id))
        else:
            flash('Username or password wrong', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<id>')
@login_required
def profile(id):
    form = AddFriendForm()
    user = User.query.get(id)
    if user is None:
        abort(404)

    user.created_at = datetime.datetime.fromtimestamp(user.created_at).strftime('%Y-%m-%d')
    if user.updated_at is not None:
        user.updated_at = datetime.datetime.fromtimestamp(user.updated_at).strftime('%Y-%m-%d %H:%M')
    is_friend = False
    is_sent = False
    is_sent_to_user = False
    is_friend = Request.is_friend(current_user, user)
    if not is_friend:
        is_sent = Request.is_sent(current_user, user)
        if is_sent:
            is_sent_to_user = Request.is_sent_to_user(current_user, user)
    return render_template('profile.html', user=user, is_friend=is_friend, is_sent=is_sent, is_sent_to_user=is_sent_to_user, form=form)


@app.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def editProfile(username):
    if current_user.id == username:
        form = EditProfileForm()
        if request.method == 'POST':
        # if form.validate_on_submit():
            timeStamp = time.time()
            user = User.query.get(username)
            user.gender = form.gender.data
            user.major = form.major.data
            user.semester = form.semester.data
            user.phone = form.phone.data
            user.mobile = form.mobile.data
            user.jabber = form.jabber.data
            user.updated_at = timeStamp
            user.about = form.about.data
            if form.picture.data.filename is not '':
                filename = secure_filename(form.picture.data.filename)
                form.picture.data.save('people' + url_for('static', filename='images/' + filename))
                user.image = filename
            db.session.commit()
            return redirect(url_for('profile', id=current_user.id))
        user = User.query.get(username)
        form.about.data = user.about
        if user is None:
            abort(404)
        filename = None
        return render_template('editProfile.html', user=user, form=form, filename=filename)
    else:
        abort(403)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = timedSerializer.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.confirmed_at = time.time()
    user.active = True

    db.session.add(user)
    db.session.commit()
    flash('Email confirmed successfully', 'success')
    return redirect(url_for('login'))

@app.route('/inbox')
def inbox():
    return render_template('notifications.html')

@app.route('/addFriend', methods=['POST'])
def addFriend():
    form = AddFriendForm()
    if form.validate_on_submit():
        fromUserId = form.fromUser.data
        toUserId = form.toUser.data
        fromUser = User.query.filter_by(id=fromUserId).first_or_404()
        toUser = User.query.filter_by(id=toUserId).first_or_404()
        if fromUser is not None and toUser is not None:
            timeStamp = time.time()
            title = 'New friendrequest'
            text = 'You have a new friendRequest from ' + fromUser.firstName + ' ' + fromUser.lastName
            friendRequest = Request(fromUser, toUser)
            notification = Notification('friendRequest', timeStamp, title, text, fromUser, toUser)
            db.session.add(notification)
            db.session.add(friendRequest)
            db.session.commit()

    return redirect(url_for('profile', id=toUserId))


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

class AddFriendForm(Form):
    fromUser = HiddenField('FromUser')
    toUser = HiddenField('ToUser')


