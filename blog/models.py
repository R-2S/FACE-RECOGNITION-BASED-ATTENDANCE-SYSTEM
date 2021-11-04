from blog import db, login_manager # Import database and login status
from flask_login import UserMixin # For create foreign Key


# Get current user id from database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create user's table into database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    full_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    varsity = db.Column(db.String(100), nullable=False)
    image_file1 = db.Column(db.String(20), nullable=False, default='avatar.png')
    image_file2 = db.Column(db.String(20), nullable=False, default='avatar.png')
    image_file3 = db.Column(db.String(20), nullable=False, default='avatar.png')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{ self.username }', '{ self.email })"
