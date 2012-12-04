# unified settings file
from pymongo import uri_parser
import os
import urlparse
class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    MONGODB_USERNAME = os.environ.get('MONGO_DB_USERNAME')#only set if exists, else None
    MONGODB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')#only set if exists, else None

class TestConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ.get('MONGO_TEST_DB')
    
class DevConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ.get('MONGO_DEV_DB')

class ProdConfig(Config):
    #empty until we get a production environment
    DEBUG = False
    mongolab_uri = os.environ.get('MONGODB_URI')
    url = uri_parser.parse_uri(mongolab_uri)
    MONGODB_USERNAME = url['username']
    MONGODB_PASSWORD = url['password']
    MONGODB_HOST,MONGODB_PORT = url['nodelist'][0]
    MONGODB_DB = url['database']
