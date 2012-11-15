from server import db

class Features(db.EmbeddedDocument):
    #TODO:implementation
    pass

class Reader(db.EmbeddedDocument):
    #TODO:implementation
    pass

class Article(db.Document):
    source_url = db.URLField(verify_exists = True)
    feed = db.ReferenceField('Feed', dbref = True)#lazily dereferenced on access
    features = db.EmbeddedDocumentField('Features')
    readers = db.ListField( db.EmbeddedDocumentField('Reader') )
