import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DATABASE.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 8080
    DEBUG = True
