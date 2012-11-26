import feedparser
from server import Article, Feed, Reader, User, Features, db
from dateutil.parser import parse

def get_readers_from(article_features, feed_subscribers):
    '''
    creates a list of reader objects for an article 
    from a list of feed subscribers
    '''
    subscribers = []
    for feed_subscriber in feed_subscribers:
        new_reader = Reader(\
                user_id = feed_subscriber.id\
                )
        subscribers.append(new_reader)
    return subscribers

def save_new_articles_from_feed(feed):
    '''save new articles from the given feed(represented by a feed object)'''
    parsed_feed = feedparser.parse(feed.rss_url)
    if parsed_feed.bozo is 1:
        #there were errors parsing the feed
        print 'Illformed XML detected for '\
                + feed.name +'('+ feed.site_url +') at '+ feed.rss_url
        return
    feed_subscribers = User.objects(subscriptions__feed_id = feed.id)
    for entry in parsed_feed.entries:
        #create new article object for this entry and save it
        article_features = Features(\
                title = entry.title\
                , content_snippet = entry.description\
                )
        new_article = Article(\
                source_url = entry.link\
                , features = article_features\
                , feed_id = feed.id\
                , time_stamp = parse(entry.published)\
                , readers = get_readers_from(article_features, feed_subscribers)\
                )
        try:
            new_article.save()
        except db.NotUniqueError:
            #we have already retrieved this article, so do nothing
            pass

if __name__ == '__main__':
    for feed in Feed.objects.all():
        save_new_articles_from_feed(feed)
