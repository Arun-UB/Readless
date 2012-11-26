from server import db
from flask.ext.mongoengine import DoesNotExist
import feedparser
import datetime

class Feed(db.Document):
    '''A document that represents the feeds we are keeping track of'''
    name = db.StringField(required = True)
    site_url = db.URLField(verify_exists = True)
    rss_url = db.URLField(verify_exists = True, unique = True, required = True)
    last_update = db.DateTimeField(default = datetime.datetime.now)#required?
    last_new_article = db.ReferenceField('Article', dbref = True)#lazily dereferenced on access

    def save(self, *args, **kwargs):
        '''
        this overrides the default save method so that the last_update field
        is set to the current time and then calls the default save method
        '''
        self.last_update = datetime.datetime.now()
        return super(Feed, self).save(*args, **kwargs)

    @staticmethod
    def get_or_construct(rssUrl):
        '''
        attempts to get a Feed object based on the rssUrl provided, in case it is not found,
        attempts to construct a new Feed object and return that
        '''
        try:
            feed = Feed.objects.get(rss_url = rssUrl)
        except DoesNotExist:
            rss_dict = feedparser.parse(rssUrl)
            if rss_dict.version is '':
                raise NotAFeed('the given url was not a recognized feed format')
            new_feed = Feed(\
                            #get title from rss feed(or atom feed)
                            name = rss_dict.feed.get('title', rss_dict['channel']['title'])\
                            #get site url from rss feed(or atom feed)
                            , site_url = rss_dict.feed.get('link', rss_dict['channel']['link'])\
                            , rss_url = rssUrl\
                            )
            new_feed.save()
            feed = new_feed
        return feed

class NotAFeed(Exception):
    pass
