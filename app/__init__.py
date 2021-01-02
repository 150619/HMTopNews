from flask import Flask
from app.settings.config import config_dict
from flask_sqlalchemy import SQLAlchemy
from common.utils.constants import EXTRA_ENV_CONFIG
from redis import StrictRedis
from app.resource.user import user_bp

db = SQLAlchemy()

redis_client = None


def register_extensions(app):
    db.init_app(app)

    global redis_client
    redis_client = StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)


def register_bp(app: Flask):
    app.register_blueprint(user_bp)


def create_flask_app(config_name):
    flask_app = Flask(__name__)
    config_class = config_dict[config_name]
    flask_app.config.from_object(config_class)
    flask_app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)
    return flask_app


def create_app(config_name):
    app = create_flask_app(config_name)
    register_extensions(app)
    register_bp(app)
    return app
