"""
  All flask server code goes here
"""
from flask import Flask, g
from flask.ext.mongoengine import MongoEngine
import settings
import os

#create the application
app = Flask(__name__)

#set the correct configuration
app.config.from_object('settings.TestConfig')#default
if os.environ.get('ENV')=='dev':
  #we are running the development server
  app.config.from_object('settings.DevConfig')

#create the db connection
db = MongoEngine(app)

#load models
import models

# load server routes
import routes
