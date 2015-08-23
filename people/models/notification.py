from people import db

class Notification(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	type = db.Column(db.Text)
	created_at = db.Column(db.Integer)
	title = db.Column(db.Text)
	text = db.Column(db.Text)
	read = db.Column(db.Boolean)
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	from_user = db.relationship('User', foreign_keys=[from_user_id])
	to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	to_user = db.relationship('User', foreign_keys=[to_user_id])

	def __init__(self, type, created_at, title, text, from_user=None, to_user=None):
		self.type = type
		self.created_at = created_at
		self.title = title
		self.text = text
		self.read = False
		self.from_user = from_user
		self.to_user = to_user

		def is_read(self):
			return self.read