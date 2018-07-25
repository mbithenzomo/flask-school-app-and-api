from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config.config import app_config

db = SQLAlchemy()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    db.init_app(app)

    return app


app = create_app("development")
api = Api(app=app, prefix="/api/v1")
from app import views
