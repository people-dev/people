from people import db 

class Profile(db.Model):
    userid = db.Column(db.Text, primary_key=True)
    about = db.Column(db.Text)
    gender = db.Column(db.Text)
    image = db.Column(db.Text)
    major = db.Column(db.Text)
    semester = db.Column(db.Text)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    mobile = db.Column(db.Text)
    jabber = db.Column(db.Text)
    street = db.Column(db.Text)
    zipcode = db.Column(db.Text)
    city = db.Column(db.Text)
    updated_at = db.Column(db.Integer)




    def __init__(self, userid, about="", gender="", image=""):
        self.userid = userid
        self.about = about
        self.gender = gender
        self.image = image

