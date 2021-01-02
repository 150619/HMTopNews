class BaseConfig:
    SECRET_KEY = '150619'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.242.134:3306/toutiao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    REDIS_HOST = '192.168.242.134'
    REDIS_PORT = 6381


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'test': TestingConfig,
}
