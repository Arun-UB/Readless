from bs4 import BeautifulSoup
import urllib
import re, argparse, sys
import nltk
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
                user_id = feed_subscriber.id \
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
                , article_words = get_words_in_article(entry.link)
                , content_snippet = get_article_snippet(entry.description,128)\
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
            print '.',
        except db.NotUniqueError:
            #we have already retrieved this article, so do nothing
            pass

def get_article_snippet(article, char_length = 128):
    '''
    Returns the article snippet to be show next to the article title.
    '''
    if(type(char_length) is int):                                   #Make sure char_length a int parameter.
        html_data = BeautifulSoup(article)                          
        pattern = re.compile('[\W_ ]+')
        words = ''.join(BeautifulSoup(article).findAll(text=True))  #Join the words from the html content.
        if len(article) < char_length:                               #Return the unedited snippet if length is less than the requested characters.
            return article + '...' 
        else:
            return article[:char_length] + '...'

def get_words_in_article(url):
    '''Arguments : URL
       Function: Gets the article only version of the URL using Instapaper.
       Extracts the text in the artcile and removes any non AlphaNumeric characters in the text
       Returns a list of words in the article present in the URL.'''
    html_data = BeautifulSoup(urllib.urlopen(
                     "http://www.instapaper.com/m?%s" % urllib.urlencode({'u':url})).read()) #URLencoding the url to pass it to Instapaper
    html_data = html_data.find("body")      #Using only the contents in HTML <body> tag, avoides Javascript from being treated as text.
    pattern = re.compile('[\W_ ]+')         #Compile regex for alphanumeric characters and spaces(for multiword strings).
    words = html_data.findAll(text=True)    #setting text to True to extract only the text in the <body>
    word_list = []                          #Stores the list of words
    for word in words[30:]:                 #Removing redundant content from Instapaper Mobilizer headers
        for w in word.split(" "):               #splitting on spcae for multiword strings
            wd = (pattern.sub('',w.lower()))    #substituing non alphanumeric characters with ''
            if len(wd) > 1 : word_list.append(wd)#exclude strings of less than 2 characters
    filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
    return dict((word,True) for word in word_list)

if __name__ == '__main__':
    print 'Starting to get Feeds'
    for feed in Feed.objects.all():
        print '\nProcessing ' + feed.name + ' '
        save_new_articles_from_feed(feed)
