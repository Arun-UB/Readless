from server import db
import datetime

class Features(db.EmbeddedDocument):
    title = db.StringField(required = True)
    content_snippet = db.StringField()

class Reader(db.EmbeddedDocument):
    user_id = db.ObjectIdField()
    score = db.FloatField(min_value = 0, max_value = 1, default = 0.5)

class Article(db.Document):
    source_url = db.URLField(verify_exists = True)
    feed_id = db.ObjectIdField()
    features = db.EmbeddedDocumentField('Features')
    readers = db.ListField(db.EmbeddedDocumentField('Reader'))
    time_stamp = db.DateTimeField(default = datetime.datetime.now())
