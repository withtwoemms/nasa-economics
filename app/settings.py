class BaseConfig(object):
    DEBUG = False
    TESTING = False

class ProdConfig(BaseConfig):
    pass

class DevConfig(BaseConfig):
    DEBUG = True
    SERVER_NAME = '127.0.0.1:8765'

class TestConfig(BaseConfig):
    TESTING = True

configs = {
    'dev'  : DevConfig,
    'test' : TestConfig,
    'prod' : ProdConfig,
    'default' : BaseConfig
}
