from server import db
from flask.ext.mongoengine import DoesNotExist
import feedparser
import datetime
import urllib
import pickle
from dateutil.parser import parse
from . import User, Article, Features, Reader


class Feed(db.Document):
    '''A document that represents the feeds we are keeping track of'''
    name = db.StringField(required = True)
    site_url = db.URLField(verify_exists = True)
    rss_url = db.URLField(verify_exists = True, unique = True, required = True)
    last_update = db.DateTimeField(default = datetime.datetime.now)
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
            if rss_dict.version == '':
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

    def update_articles(self):
        '''Update articles for the Feed'''
        parsed_feed = feedparser.parse(self.rss_url)
        if parsed_feed.bozo is 1:
            #there were errors parsing the feed
            print 'Illformed XML detected for '\
                    + feed.name +'('+ feed.site_url +') at '+ self.rss_url
            return
        if self.last_new_article != None:
            #last_new_article exists
            last_link_from_previous_run = self.last_new_article.source_url
        else:
            last_link_from_previous_run = None
        for entry in parsed_feed.entries:
            #create new article object for this entry and save it,
            #if it's not  the last new article
            if entry.link == last_link_from_previous_run:
                #we have this article already
                print "found last_link_from_previous_run"
                break
            new_article = Article(\
                    source_url = entry.link\
                    , feed_id = self.id\
                    , time_stamp = parse(entry.published)\
                    )
            article_features = Features(\
                    title = entry.title\
                    , content_snippet = new_article.get_article_snippet(entry.description,128)\
                    )
            new_article.features = article_features
            new_article.readers = new_article.get_readers_from()
            try:
                new_article.save()
                self.last_new_article = new_article
                print '+',
            except db.ValidationError as e:
                print 'Validation error occured'
                if e.errors.get('source_url'):
                    print new_article.source_url+" may be broken."
            except db.NotUniqueError:
                #we have already retrieved this article, so do nothing
                print '.'
        #save to keep track of the last new article, so no need to validate
        self.save(validate = False)

class NotAFeed(Exception):
    '''Thrown if attempt is made to create a feed object from a non-feed url'''
    pass
