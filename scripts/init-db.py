import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from people import db
import people.models

db.drop_all()
db.create_all()
db.session.commit()