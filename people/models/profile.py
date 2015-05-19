from people import db 

class Profile(db.Model):
    userid = db.Column(db.Text, primary_key=True)
    aboutText = db.Column(db.Text)
    gender = db.Column(db.Text)
    image = db.Column(db.Text)




    def __init__(self, userid, aboutText, gender, image):
        self.userid = userid
        self.aboutText = aboutText
        self.gender = gender
        self.image = image

