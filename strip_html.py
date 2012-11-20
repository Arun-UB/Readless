from bs4 import BeautifulSoup
import urllib
import re, argparse, sys
import string
from nltk.classify import PositiveNaiveBayesClassifier
import nltk


def get_words_in_article(url):
    '''Arguments : URL
       Function: Gets the article only version of the URL using Instapaper. Extracts the text in the artcile and removes any non AlphaNumeric characters in the text
       Returns a list of words in the article present in the URL.'''
    html_data = BeautifulSoup(urllib.urlopen("http://www.instapaper.com/m?%s" % urllib.urlencode({'u':url})).read()) #URLencoding the url to pass it to Instapaper
    html_data = html_data.find("body") 		#Using only the contents in HTML <body> tag, avoides Javascript from being treated as text.
    pattern = re.compile('[\W_ ]+')    		#Compile regex for alphanumeric characters and spaces(for multiword strings).
    words = html_data.findAll(text=True)	#setting text to True to extract only the text in the <body>
    word_list = []				#Stores the list of words
    for word in words[30:]:			#Removing redundant content from Instapaper Mobilizer headers
	for w in word.split(" "):		#splitting on spcae for multiword strings
	    wd = (pattern.sub('',w.lower()))	#substituing non alphanumeric characters with ''
	    if len(wd) > 1 : word_list.append(wd)#exclude 0 & 1 character strings
    filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
    return dict((word,True) for word in word_list)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Accepts a URL")
    parser.add_argument("--url",dest = "url") #Extracts url from command line, if available
    urls = parser.parse_args()
    if urls.url == None:
        print ("No URL Specified")
        sys.exit()
    positive_examples = map(get_words_in_article, ['http://www.engadget.com/2012/11/16/htc-droid-dna-review/', 'http://www.engadget.com/2012/10/08/samsung-galaxy-note-ii-review/', 'http://www.engadget.com/2012/11/16/htc-desire-x-review/', 'http://www.engadget.com/2012/11/16/htc-desire-x-review/'])
    misc_examples = map(get_words_in_article, ['http://www.engadget.com/2012/11/16/sharp-aquos-sh930w-reviewed-early-in-russia-with-1080p-display/', 'http://www.engadget.com/2012/11/15/nexus-4-backordered/', 'http://www.engadget.com/2012/11/16/htc-windows-phone-8x-t-mobile-review/', 'http://www.engadget.com/2012/11/16/distro-issue-66-holiday-gift-guide/', 'http://www.engadget.com/2012/10/29/apple-macbook-pro-with-retina-display-review-13-inch/', 'http://www.engadget.com/2012/11/17/skydrive-sdk-net-windows-phone-8/'])
    classifier = PositiveNaiveBayesClassifier.train(positive_examples,misc_examples)

    print classifier.classify(get_words_in_article(urls.url))
