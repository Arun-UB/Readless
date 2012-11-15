from server import db

class Feed(db.Document):
    name = db.StringField(required = True)
    site_url = db.URLField(verify_exists = True)
    rss_url = db.URLField(verify_exists = True)
    last_update = db.DateTimeField()#required?
    last_new_article = db.ReferenceField('Article', dbref = True)#lazily dereferenced on access
