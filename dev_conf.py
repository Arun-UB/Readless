'''
  The db setup when running as a development server
'''
import os
DATABASE = os.environ['MONGO_DEV_DB']
DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
USERNAME = os.environ['MONGO_DB_USERNAME']
PASSWORD = os.environ['MONGO_DB_PASSWORD']
