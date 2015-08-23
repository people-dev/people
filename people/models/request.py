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