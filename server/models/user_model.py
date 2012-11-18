from server import db
from flask.ext.login import UserMixin

class Subscription(db.EmbeddedDocument):
    '''
    a passable implementation
    TODO: need to add other fields for storing classifier
    '''
    feed_id = db.ObjectIdField()
    category = db.StringField()

class User(db.Document, UserMixin):
    name = db.StringField(required = True)
    email = db.EmailField(required = True, unique = True)
    password_hash = db.StringField(max_length = 160)
    subscriptions = db.ListField(db.EmbeddedDocumentField(Subscription))
