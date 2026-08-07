import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_NAME = os.environ.get("POSTGRES_DB")
    DATABASE_USER = os.environ.get("POSTGRES_USER")
    DATABASE_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DATABASE_PORT = os.environ.get("POSTGRES_PORT")
    DATABASE_HOST = os.environ.get("POSTGRES_HOST")
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
