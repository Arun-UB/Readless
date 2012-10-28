"""
  All flask server code goes here
"""
from pymongo import Connection
from pymongo.errors import AutoReconnect
from flask import Flask, g
import settings

#create the application
app = Flask(__name__)

@app.before_request
def before_request():
  # get a connection and set the db object up before each request
  try:#to use the configured server
    server=app.config['SERVER']
  except KeyError:#unless you can't
    server='localhost'
  mongodburi='mongodb://%(username)s:%(password)s@%(server)s/%(database)s' % \
      {
          "username":app.config['USERNAME'], 
          "password":app.config['PASSWORD'],
          "database":app.config['DATABASE'],
          "server":server
          }

  try:
    g.connection = Connection(host = mongodburi)
  except AutoReconnect:#might occur
    #and i'm supposed to just let it
    pass

  g.db = g.connection[app.config['DATABASE']]

@app.teardown_request
def teardown_request(exception):
  #called if exception is raised
  g.connection.close()
  g.db = None #not sure if required, but doesn't hurt

@app.after_request
def after_request(response):
  #must always return a response and take one
  g.connection.close()
  g.db = None
  return response

#set the correct config and decide what to  do
if __name__ == '__main__':
  #we are running the server
  app.config.from_object('settings.DevConfig')
  app.run()
else:
  #looks like we aren't a server
  app.config.from_object('settings.TestConfig')
