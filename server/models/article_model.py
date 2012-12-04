from bs4 import BeautifulSoup
from server import db
from . import User
import datetime
import urllib
import re
import nltk
import pickle

class Features(db.EmbeddedDocument):
    '''An embedded document that represents the features of an article'''
    title = db.StringField(required = True)
    article_words = db.DictField()
    content_snippet = db.StringField()

class Reader(db.EmbeddedDocument):
    '''
    An embedded document that represents a user who hasn't read this article yet
    and his predicted interest level for this article
    '''
    user_id = db.ObjectIdField()
    score = db.FloatField(min_value = 0, max_value = 1, default = 0.5)

class Article(db.Document):
    '''A document that represents an article extracted from a feed'''
    source_url = db.URLField(verify_exists = True, unique = True)
    feed_id = db.ObjectIdField()
    features = db.EmbeddedDocumentField('Features')
    readers = db.ListField(db.EmbeddedDocumentField('Reader'))
    interested_users = db.ListField(db.ObjectIdField())
    uninterested_users = db.ListField(db.ObjectIdField())
    time_stamp = db.DateTimeField(default = datetime.datetime.now())

    def get_words_in_article(self):
        '''
        Arguments : URL
        Function: Gets the article only version of the URL using Instapaper.
        Extracts the text in the artcile and removes any non AlphaNumeric characters in the text
        Returns a list of words in the article present in the URL.'''
        #get article content from instapaper
        html_data = BeautifulSoup(urllib.urlopen(
            "http://www.instapaper.com/m?%s" % urllib.urlencode({'u':self.source_url})).read())
        html_data = html_data.find("body")

        content = html_data.findAll(text=True)  #setting text to True to extract only the text in the <body>

        word_list = []
        for word in content[30:]:               #Removing redundant content from Instapaper Mobilizer headers
            for w in word.split(" "):           #splitting on spcae for multiword strings
                wd = (multiword_string_pattern.sub('',w.lower()))    #substituing non alphanumeric characters with ''
                if len(wd) > 1 : word_list.append(wd)#exclude strings of less than 2 characters
        filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
        return dict((word,True) for word in word_list)

    def get_words_in_title(self):
        "Get words in the title of an article"
        word_list = []
        for w in self.features.title.split(" "):
            wd = (multiword_string_pattern.sub('',w.lower()))    
            if len(wd) > 1 : word_list.append(wd)
        filtered_words = [w for w in word_list if w not in nltk.corpus.stopwords.words('english')]
        return dict((word,True) for word in filtered_words)

    def get_score(self,classifier_object):
        "Use the trained classifier to find the interest for the new article"
        if classifier_object is None:
            return 0.5
        classifier = pickle.loads(classifier_object)
        if classifier.classify(self.get_words_in_title()) is True:
            return 1
        else:
            return 0

    def get_readers_from(self):
        '''
        creates a list of reader objects for an article 
        from a list of feed subscribers
        '''
        subscribers = []
        feed_subscribers = User.objects(subscriptions__feed_id = self.feed_id)
        for feed_subscriber in feed_subscribers:
            classifier_object = None
            for subscription in feed_subscriber.subscriptions:
                if subscription.feed_id == self.feed_id:
                    classifier_object = subscription.classifier_object
            new_reader = Reader(\
                    user_id = feed_subscriber.id \
                    , score = self.get_score(classifier_object)
                    )   #Set the scores for each user who has not yet read the article
            subscribers.append(new_reader)
        return subscribers

    def get_article_snippet(self,article, max_length = 128):
        '''
        Returns the article snippet to be show next to the article title.
        '''
        #Make sure char_length a int parameter.
        if(type(max_length) is not int):
            max_length = 128
        html_data = BeautifulSoup(article)                          
        #Join the words from the html content.
        words = ''.join(html_data.findAll(text=True))
        if len(article) < max_length:
            return words + '...' 
        else:
            return words[:max_length] + '...'


#Compile regex for alphanumeric characters and spaces(for multiword strings).
multiword_string_pattern = re.compile('[\W_ ]+')
