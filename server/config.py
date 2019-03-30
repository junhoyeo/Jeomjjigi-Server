import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DATABASE.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET_KEY = os.urandom(24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = False


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 8080
    DEBUG = True
