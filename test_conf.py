'''
  The db setup when not running as a development server(like for unit tests)
'''
import os
DATABASE = os.environ['MONGO_TEST_DB']
DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
USERNAME = os.environ['MONGO_DB_USERNAME']
PASSWORD = os.environ['MONGO_DB_PASSWORD']
