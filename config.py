import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('TRACK_MODIFICATIONS', False)
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')