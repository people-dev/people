from people import db 

class Profile(db.Model):
    userid = db.Column(db.Text, primary_key=True)
    about = db.Column(db.Text)
    gender = db.Column(db.Text)
    image = db.Column(db.Text)
    mayor = db.Column(db.Text)
    semester = db.Column(db.Text)
    updated_at = db.Column(db.Integer)




    def __init__(self, userid, about="", gender="", image=""):
        self.userid = userid
        self.about = about
        self.gender = gender
        self.image = image

