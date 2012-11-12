"""
  All flask server code goes here
"""
from pymongo import Connection
from pymongo.errors import AutoReconnect
from flask import Flask, g
import settings

def create_db_connection(config):
  try:#to use the configured server
    server=config['MONGO_SERVER']
  except KeyError:#unless you can't
    server='localhost'
  mongodburi='mongodb://%(username)s:%(password)s@%(server)s/%(database)s' % \
      {
          "username":config['MONGO_USERNAME'], 
          "password":config['MONGO_PASSWORD'],
          "database":config['MONGO_DBNAME'],
          "server":server
          }

  try:
    connection = Connection(host = mongodburi)
  except AutoReconnect:#might occur
    #and i'm supposed to just let it
    pass

  db = connection[config['MONGO_DBNAME']]
  return db

#create the application
app = Flask(__name__)

#set the correct configuration
if __name__ == '__main__':
  #we are running the server
  app.config.from_object('settings.DevConfig')
else:
  #looks like we aren't a server
  app.config.from_object('settings.TestConfig')

#create the db connection
db = create_db_connection(app.config)

#start the server if required
if __name__ == '__main__':
  app.run()
