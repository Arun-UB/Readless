from models import Feed

def update():
    """Update articles from all feeds"""
    print 'Starting to get Feeds'
    for feed in Feed.objects.all():
        print '\nProcessing ' + feed.name + ' '
        feed.save_new_articles_from_feed()