from people import db

class Notification(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user = db.Column(db.Text)
	notificationType = db.Column(db.Text)
	notificationTime = db.Column(db.Integer)
	notificationText = db.Column(db.Text)
	read = db.Column(db.Boolean)

	def __init__(self, user, notificationType, notificationTime, notificationText):
		self.user = user
		self.notificationType = notificationType
		self.notificationTime = notificationTime
		self.notificationText = notificationText
		self.read = False


		def is_read(self):
			return self.read