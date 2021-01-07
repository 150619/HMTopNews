from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建mysql数据库对象
db = SQLAlchemy()

# 创建redis数据库对象
redis_client = None


# 注册扩展组件
def register_extensions(app: Flask):
    # 关联flask应用
    db.init_app(app)

    # 创建redis数据库对象,decode_response=True
    global redis_client
    from redis import StrictRedis
    redis_client = StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)

    # 注册路由转换器
    from common.utils.converters import register_converters
    register_converters(app)

    # 迁移
    from flask_migrate import Migrate
    Migrate(app, db)
    from common.models import user, article

    # 添加请求钩子
    from common.utils.middlewares import get_user_info
    app.before_request(get_user_info)


# 注册蓝图组件
def register_bp(app: Flask):
    from app.resource.user import user_bp
    app.register_blueprint(user_bp)
    from app.resource.channel import channel_bp
    app.register_blueprint(channel_bp)


# 内部调用创建app工厂的方法
def create_flask_app(config_name):
    # 创建flask_app对象
    flask_app = Flask(__name__)

    # 读取配置类中的配置信息
    from app.settings.config import config_dict
    config_class = config_dict[config_name]
    flask_app.config.from_object(config_class)

    # 读取环境变量中的配置信息
    from common.utils.constants import EXTRA_ENV_CONFIG
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
