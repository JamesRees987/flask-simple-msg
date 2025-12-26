from os import getenv
from urllib.parse import quote_plus

from flask_sqlalchemy import SQLAlchemy

def loadDb():
    return {
        "user": getenv("simple_msg_database_user"),
        "password": getenv("simple_msg_database_key"),
        "host": getenv("simple_msg_database_host"),
        "name": getenv("simple_msg_database_database"),
        "port": getenv("simple_msg_database_port", "5432"),
    }

def getUrl(creds=None):
    if creds is None:
        creds = loadDb()
    password = quote_plus(creds["password"]) if creds.get("password") else ""
    return f"postgresql://{creds['user']}:{password}@{creds['host']}:{creds['port']}/{creds['name']}"

dbCreds = loadDb()
dbUrl = getUrl(dbCreds)

db = SQLAlchemy()