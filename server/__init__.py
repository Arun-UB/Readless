"""
  All flask server code goes here
"""
from flask import Flask, g
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
import os
import logging
from logging import FileHandler

#create the application
app = Flask(__name__)

# overriding default jinja template tags, to avoid conflicts with angularjs
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

#set the correct configuration
if os.environ.get('ENV')=='dev':
  #we are running the development server
  app.config.from_object('settings.DevConfig')

if os.environ.get('ENV')=='pro':
  #we are running the development server
  app.config.from_object('settings.ProdConfig')

#create the db connection
db = MongoEngine(app)

#set up login manager
login_manager = LoginManager()
login_manager.setup_app(app)

#set url to redirect to for login
login_manager.login_view = '/signin'

#create a log handler and attach it to app
handler = FileHandler('app.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

#load models
from models import User, Article, Feed, Reader, Features

#setting up user_loader callback, for Flask login
@login_manager.user_loader
def load_user(userid):
    return User.objects.get(id = userid)

# load server routes
import routes
