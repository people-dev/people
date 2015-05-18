from people import db, app 
from people.models.user import User
from flask.ext.login import LoginManager


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id` 
    # 2. Create a new object of `User` class and return it.
    return User.query.get(id)