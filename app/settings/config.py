# 配置父类
class BaseConfig:
    # 加密密钥
    SECRET_KEY = '150619'

    # JWT
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
    JWT_EXPIRE_DAYS = 14

    # mysql数据库的配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@192.168.242.134:3306/Hmtop'
    # 数据库修改跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 底层输出sql语句
    SQLALCHEMY_ECHO = False

    # redis数据库的配置信息
    REDIS_HOST = '192.168.242.134'
    REDIS_PORT = 6381


# 开发模式配置信息
class DevelopmentConfig(BaseConfig):
    pass


# 测试模式配置信息
class TestingConfig(BaseConfig):
    pass


# 生产模式配置信息
class ProductionConfig(BaseConfig):
    pass


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'test': TestingConfig,
}
