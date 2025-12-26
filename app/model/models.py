from model.db import db
from flask_login import UserMixin

class UserCreds(db.Model, UserMixin):
    __tablename__ = "userCreds"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    profile_image = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self) -> str:
        return f"<UserCreds id={self.id} username={self.username!r}>"
    
class User(UserCreds, UserMixin):
    """Wrapper class to add Flask-Login functionality to UserCreds"""
    pass
