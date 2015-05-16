from people import db, roles_users
from sqlalchemy.orm import validates
import re

class User(db.Model):
    id = db.Column(db.Text, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))



    def __init__(self, id, firstName, lastName, password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = id + "@informatik.uni-hamburg.de"
        self.password = password
        self.active = False
        self.confirmed_at = ""

    @validates("id")
    def validate_id(self, key, id):
        assert re.match("^[0-9]{2}[a-z]{1,7}$", id)
        return id

