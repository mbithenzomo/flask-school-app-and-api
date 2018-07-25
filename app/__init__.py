import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config.config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app


app = create_app(os.getenv('ENVIRONMENT'))
api = Api(app=app, prefix="/api/v1")
from app import views
