from server import Feed

def update():
    """Update articles from all feeds"""
    print 'Starting to get Feeds'
    for feed in Feed.objects.all():
        print '\nProcessing ' + feed.name + ' '
        feed.update_articles()

if __name__ == '__main__':
	update()