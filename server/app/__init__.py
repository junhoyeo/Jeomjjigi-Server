from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

from config import DevConfig


def create_app():
    _app = Flask(__name__)
    CORS().init_app(_app)

    _app.secret_key = os.urandom(24)
    _app.logger.propagate = True
    _app.config.from_object(DevConfig)
    return _app


app = create_app()
db = SQLAlchemy(app)
Migrate().init_app(app, db)

from app.views import api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')
