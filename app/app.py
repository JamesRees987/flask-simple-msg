from flask import Flask
from routes.routes import route
from routes.auth import auth
from routes.chats import chat
from os import getenv
from flask_login import LoginManager
from model.models import User
from flask_socketio import SocketIO

# set PYTHONDONTWRITEBYTECODE=1
import sys
sys.dont_write_bytecode = True

# Logging setup
import logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Load database configuration, connection URL, and SQLAlchemy instance from model.db
from model.db import dbCreds, dbUrl, db

app = Flask(__name__)

# Register blueprints
app.register_blueprint(route)
app.register_blueprint(auth)
app.register_blueprint(chat)

class Config:
    # Flask settings
    SECRET_KEY = getenv("simple_msg_flask_secret_key", "set_a_real_secret_key")
    DEBUG = getenv("FLASK_DEBUG", "false").lower() == "true"

    # Database settings
    SQLALCHEMY_DATABASE_URI = dbUrl
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800
    }
    DB_CREDENTIALS = dbCreds

    # LoginManager settings
    LOGIN_VIEW = 'auth.signIn'
    LOGIN_MESSAGE = 'Please log in to access this page.'

    # SocketIO settings
    SOCKETIO_CORS_ALLOWED_ORIGINS = getenv("CORS_ORIGINS", "*").split(",")

app.config.from_object(Config)

# Initialize db with app
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = app.config["LOGIN_VIEW"]
login_manager.login_message = app.config["LOGIN_MESSAGE"]

# SocketIO setup
socketio = SocketIO(
    app, cors_allowed_origins=app.config["SOCKETIO_CORS_ALLOWED_ORIGINS"])

if __name__ == "__main__":
    import model.models  # import models to register them with SQLAlchemy
    with app.app_context():
        logging.info("Creating database tables if not exist...")
        db.create_all()
        logging.info("Database tables created or already exist.")
    socketio.run(app, debug=app.config["DEBUG"])
