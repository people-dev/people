import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from people import db
from people.models import User, Profile, Notification
from werkzeug.security import generate_password_hash
import time

db.drop_all()
db.create_all()

ts= time.time()

user = User("00admin", "Admin", "Account", generate_password_hash("plaintextpassword"),ts)
user.active = True
user.confirmed_at = ts

profile = Profile("00admin")

notification = Notification(user.id, "Info", ts, "Hello People", "Test notification")

db.session.add(user)
db.session.add(profile)
db.session.add(notification)

db.session.commit()
