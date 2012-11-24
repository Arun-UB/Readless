from server import db
from flask.ext.login import UserMixin

class Subscription(db.EmbeddedDocument):
    '''
    TODO: need to add other fields for storing classifier
    '''
    feed_id = db.ObjectIdField()

class User(db.Document, UserMixin):
    '''
    A class that represents users who will use this system, their subscriptions
    and is used to manage their sessions
    '''
    name = db.StringField(required = True)
    email = db.EmailField(required = True, unique = True)
    password_hash = db.StringField(max_length = 160)
    subscriptions = db.ListField(db.EmbeddedDocumentField(Subscription))
