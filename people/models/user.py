from people import db
from .request import Request
from sqlalchemy.orm import validates
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re


class User(db.Model, UserMixin):
    id = db.Column(db.Text, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default = False)
    confirmed_at = db.Column(db.Integer)
    created_at = db.Column(db.Integer)
    about = db.Column(db.Text)
    gender = db.Column(db.Text)
    image = db.Column(db.Text)
    major = db.Column(db.Text)
    semester = db.Column(db.Text)
    phone = db.Column(db.Text)
    mobile = db.Column(db.Text)
    jabber = db.Column(db.Text)
    street = db.Column(db.Text)
    zipcode = db.Column(db.Text)
    city = db.Column(db.Text)
    updated_at = db.Column(db.Integer, nullable=True)

    privacy_protected_columns = (
        'firstName', 'lastName', 'email', 'about',
        'gender', 'image', 'major', 'semester',
        'phone', 'mobile', 'jabber', 'street',
        'zipcode', 'city', 'created_at', 'updated_at',
        'full_name')

    def __init__(self, id, firstName, lastName, password, created_at):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = id + "@informatik.uni-hamburg.de"
        self.password = password
        self.confirmed_at = 0
        self.created_at = created_at

    @validates("id")
    def validate_id(self, key, id):
        try:
            assert re.match("^[0-9]{2}[a-z]{1,7}$", id)
        except Exception as inst:
            return False;
        else:
            return id

    def get_attributes_visible_for(self, user):
        if user.is_authenticated and Request.is_friend(self, user):
            return self.__dict__
        else:
            return {column: getattr(self, column) for column in self.privacy_protected_columns if self.get_column_privacy(column) == 'public'}

    def get_column_privacy(self, column):
        return getattr(self, column+'_privacy')

    @property
    def full_name(self):
        return self.firstName + self.lastName

    @property
    def address(self):
        return self.street + '\n' + \
            self.zipcode + self.city

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

for column in User.privacy_protected_columns:
    setattr(User, column + '_privacy', db.Column(db.Enum('public', 'friends'), default = 'friends'))
