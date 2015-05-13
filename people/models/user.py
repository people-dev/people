from people import db
from sqlalchemy.orm import validates
import re

class User(db.Model):
	id = db.Column(db.Text, primary_key=True)

	def __init__(self, id):
		self.id = id

	@validates("id")
	def validate_id(self, key, id):
		assert re.match("^[0-9]{2}[a-z]{1,7}$", id)
		return id

