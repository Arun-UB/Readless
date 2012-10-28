# unified settings file
import os
class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    USERNAME = os.environ['MONGO_DB_USERNAME']
    PASSWORD = os.environ['MONGO_DB_PASSWORD']

class TestConfig(Config):
    DEBUG = True
    DATABASE = os.environ['MONGO_TEST_DB']

class DevConfig(Config):
    DEBUG = True
    DATABASE = os.environ['MONGO_DEV_DB']

class ProdConfig(Config):
#empty until we get a production environment
    DEBUG = False
