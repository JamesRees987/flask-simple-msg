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
    
    # ADD THIS RELATIONSHIP
    chats = db.relationship('UserToChat', back_populates='user', lazy=True)
    messages = db.relationship('Message', back_populates='sender', lazy=True)
    
    def __repr__(self) -> str:
        return f"<UserCreds id={self.id} username={self.username!r}>"
    
class User(UserCreds, UserMixin):
    """Wrapper class to add Flask-Login functionality to UserCreds"""
    pass

class UserToChat(db.Model):
    __tablename__ = "userToChat"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userCreds.id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    
    # ADD THESE RELATIONSHIPS
    user = db.relationship('UserCreds', back_populates='chats')
    chat = db.relationship('Chat', back_populates='users')
    
    def __repr__(self) -> str:
        return f"<UserToChat id={self.id} user_id={self.user_id} chat_id={self.chat_id}>" 
    
class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    chat_name = db.Column(db.String(150), nullable=True)
    chat_image = db.Column(db.LargeBinary, nullable=True)
    
    # ADD THESE RELATIONSHIPS
    users = db.relationship('UserToChat', back_populates='chat', lazy=True)
    messages = db.relationship('Message', back_populates='chat', lazy=True)
    
    def __repr__(self) -> str:
        return f"<Chat id={self.id}>"

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("userCreds.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    # ADD THESE RELATIONSHIPS
    chat = db.relationship('Chat', back_populates='messages')
    sender = db.relationship('UserCreds', back_populates='messages')
    
    def __repr__(self) -> str:
        return f"<Message id={self.id} chat_id={self.chat_id} sender_id={self.sender_id}>"