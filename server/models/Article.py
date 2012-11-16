from server import db

class Features(db.EmbeddedDocument):
    #TODO:implementation
    pass

class Reader(db.EmbeddedDocument):
    user = db.ReferenceField('User', dbref = False)# the false setting here will make mongoengine use ObjectId strings here, i think
    score = db.FloatField(min_value = 0, max_value = 1, default = 0.5)

class Article(db.Document):
    source_url = db.URLField(verify_exists = True)
    feed_id = db.ObjectIdField()
    features = db.EmbeddedDocumentField('Features')
    readers = db.ListField(db.EmbeddedDocumentField('Reader'))
