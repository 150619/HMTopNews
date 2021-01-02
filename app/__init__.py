from flask import Flask
from app.settings.config import config_dict
from flask_sqlalchemy import SQLAlchemy
from common.utils.constants import EXTRA_ENV_CONFIG
from redis import StrictRedis
from app.resource.user import user_bp

# 创建数据库对象
db = SQLAlchemy()

# 创建redis数据库对象
redis_client = None


# 注册扩展组件
def register_extensions(app: Flask):
    # 数据库对象关联app,延后关联
    db.init_app(app)

    # 创建redis数据库对象,decode_response=True
    global redis_client
    redis_client = StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)


# 注册蓝图组件
def register_bp(app: Flask):
    app.register_blueprint(user_bp)


# 内部调用创建app工厂的方法
def create_flask_app(config_name):
    # 创建flask_app对象
    flask_app = Flask(__name__)
    # 读取配置类中的配置信息
    config_class = config_dict[config_name]
    flask_app.config.from_object(config_class)
    # 读取环境变量中的配置信息
    flask_app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)
    return flask_app


# 提供一个给外界调用的创建app的方法
def create_app(config_name):
    # 创建app对象
    app = create_flask_app(config_name)
    # 注册扩展组件
    register_extensions(app)
    # 注册蓝图组件
    register_bp(app)
    return app
