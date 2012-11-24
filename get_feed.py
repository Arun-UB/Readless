#import strip_html
import feedparser
import json
import sys

def get_feed(url):
	feed = feedparser.parse(url)
	if len(feed.feed) is 0:
		print ("Error in feed URL, check feed url/network connectivity")
		sys.exit(0)
	ret = {'articles':[]}
	
	for item in feed.entries:
		ret['articles'].append((item.title,item.link,item.description))
	print json.dumps(ret['articles'][0])

if __name__ == '__main__':
	get_feed('http://feeds.feedburner.com/Phoronix')#"http://www.engadget.com/rss.xml")