from server import db
import datetime

class Feed(db.Document):
    name = db.StringField(required = True)
    site_url = db.URLField(verify_exists = True)
    rss_url = db.URLField(verify_exists = True)
    last_update = db.DateTimeField(default = datetime.datetime.now)#required?
    last_new_article = db.ReferenceField('Article', dbref = True)#lazily dereferenced on access

    def save(self, *args, **kwargs):
        '''
        this overrides the default save method so that the last_update field is set to the current time and then calls the default save method
        '''
        self.last_update = datetime.datetime.now
        return super(Feed, self).save(*args, **kwargs)
