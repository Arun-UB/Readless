import strip_html
import feedparser

def get_feed(url):
	feed = feedparser.parse(url)
	if len(feed.feed) is 0:
		print ("Error in feed URL, check feed url/network connectivity")
	for item in feed.entries:
		print strip_html.strip_html(item.link)

if __name__ == '__main__':
	get_feed("http://www.engadget.com/rss.xml")
