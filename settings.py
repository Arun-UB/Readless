# unified settings file
import os
class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    MONGODB_USERNAME = os.environ['MONGO_DB_USERNAME']
    MONGODB_PASSWORD = os.environ['MONGO_DB_PASSWORD']

class TestConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ['MONGO_TEST_DB']

class DevConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ['MONGO_DEV_DB']

class ProdConfig(Config):
#empty until we get a production environment
    DEBUG = False
