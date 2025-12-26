from flask import Flask
from routes.routes import route
from routes.auth import auth
from routes.chats import chat
from os import getenv
from flask_login import LoginManager
from model.models import User
from flask_socketio import SocketIO

import sys
sys.dont_write_bytecode = True

# Log setup
import logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Load database configuration, connection URL, and SQLAlchemy instance from model.db
from model.db import dbCreds, dbUrl, db

app = Flask(__name__)

# Register blueprints
app.register_blueprint(route)
app.register_blueprint(auth)
app.register_blueprint(chat)

# Expose credentials on app config for other modules if needed
app.config["DB_CREDENTIALS"] = dbCreds

# Set SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = dbUrl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = getenv("simple_msg_flask_secret_key", "set_a_real_secret_key")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 1800}

# Initialize db with app
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signIn'  # Redirect to login page if not authenticated
login_manager.login_message = 'Please log in to access this page.'

# SocketIO setup
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    import model.models  # import models to register them with SQLAlchemy
    with app.app_context():
        logging.info("Creating database tables if not exist...")
        db.create_all()
        logging.info("Database tables created or already exist.")
    socketio.run(app, debug=True)
