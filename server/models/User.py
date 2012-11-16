from server import db
from flask.ext.login import UserMixin

class Subscription(db.EmbeddedDocument):
    '''
    a passable implementation, need to add other fields for storing classifier
    '''
    feed = db.ReferenceField('Feed', dbref = True)#lazily dereferenced on access
    category = db.StringField()

class User(db.Document):
    name = db.StringField(required = True)
    email = db.EmailField(required = True, unique = True)
    password_hash = db.StringField(max_length = 160)
    subscriptions = db.ListField(db.EmbeddedDocumentField(Subscription))

