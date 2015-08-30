from people import db

class Request(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	accepted = db.Column(db.Boolean)
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	from_user = db.relationship('User', foreign_keys=[from_user_id])
	to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	to_user = db.relationship('User', foreign_keys=[to_user_id])

	def __init__(self, from_user, to_user):
		self.accepted = False
		self.from_user = from_user
		self.to_user = to_user

	def is_accepted(self):
		return self.accepted

	@classmethod
	def is_friend(cls, user1, user2):
		return db.session.query(Request).filter(((cls.from_user == user1) & (cls.to_user == user2) | (cls.from_user == user2) & (cls.to_user == user1)) & (cls.accepted == True)).count()

	@classmethod
	def is_sent(cls, user1, user2):
		return db.session.query(Request).filter(((cls.from_user == user1) & (cls.to_user == user2) | (cls.from_user == user2) & (cls.to_user == user1)) & (cls.accepted == False)).count()

	@classmethod	
	def is_sent_to_user(cls, user1, user2):
		return db.session.query(Request).filter((cls.from_user == user2) & (cls.to_user == user1) & (cls.accepted == False)).count()
