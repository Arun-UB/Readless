# unified settings file
import os
import urlparse
class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    MONGODB_USERNAME = os.environ.get('MONGO_DB_USERNAME')#only set if exists, else None
    MONGODB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')#only set if exists, else None

class TestConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ['MONGO_TEST_DB']

class DevConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ['MONGO_DEV_DB']

class ProdConfig(Config):
    #empty until we get a production environment
    DEBUG = False
    def __init__(self):
        mongolab_uri = os.environ.get('MONGODB_URI')
        if mongolab_uri != None:
            url = urlparse.urlparse(mongolab_uri)
            self.MONGODB_USERNAME = url.username
            self.MONGODB_PASSWORD = url.password
            self.MONGODB_HOST = url.hostname
            self.MONGODB_PORT = url.port
            self.MONGODB_DB = url.path[1:]
