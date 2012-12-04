#try classifier
import re
from strip_html import get_words_in_article
from nltk.classify import PositiveNaiveBayesClassifier
from nltk import clean_html
import urllib
from server import app, db
from flask.ext.mongoengine import DoesNotExist, ValidationError
from server import User, Feed, Article, Reader
import nltk
import pprint
import pickle

pattern = re.compile('[\W_ ]+')

def get_words_in_title(title):
    word_list = []
    for w in title.split(" "):
        wd = (pattern.sub('',w.lower()))    
        if len(wd) > 1 : word_list.append(wd)
    filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
    return dict((word,True) for word in filtered_words)


def train():
    """Train the clasifier"""
    words = {}
    
    for user in User.objects.all():
        print 'Training for User ' + str(user.id),
        for subscription in user.subscriptions:
            interested_titles_list = []
            unlabled_titles_list = []
            for article in Article.objects(interested_users = user.id, feed_id = subscription.feed_id):
                    interested_titles_list.append(article.features.title)
                    unlabled_titles_list.append(article.features.title)
            for article in Article.objects(uninterested_users = user.id, feed_id = subscription.feed_id):
                    unlabled_titles_list.append(article.features.title)
            words = map(get_words_in_title,interested_titles_list)
            print interested_titles_list
            classifier = PositiveNaiveBayesClassifier.train(words,map(get_words_in_title,unlabled_titles_list)) 
            subscription.classifier_object = pickle.dumps(classifier)
        try: 
            user.save()
        except Exception as e:
            print 'Failed: %s' % e
        print 'Classifier Saved'

if __name__ == '__main__':
    train()