import nltk,re,urllib
from bs4 import BeautifulSoup
import strip_html
from nltk.classify import NaiveBayesClassifier

pattern = re.compile('[\W_ ]+')	#Compile regex for alphanumeric characters and spaces(for multiword strings).

def get_list_of_words_in_url(url):
	"""Returns a list of words in the article present in the article,
	 after processing the article with Instapaper."""
	html_data = BeautifulSoup(urllib.urlopen(
				"http://www.instapaper.com/m?%s" % urllib.urlencode({'u':url})).read()) #URLencoding the url to pass it to Instapaper
	html_data = html_data.find("body") 		#Using only the contents in HTML <body> tag, avoides Javascript from being treated as text.
	words = html_data.findAll(text=True)	#setting text to True to extract only the text in the <body>
	word_list = []				            #Stores the list of words
	for word in words[30:]:			        #Removing redundant content from Instapaper Mobilizer headers
		for w in word.split(" "):		        #splitting on spcae for multiword strings
			wd = (pattern.sub('',w.lower()))	#substituing non alphanumeric characters with ''
			if len(wd) > 1 and not wd.isdigit(): word_list.append(wd)#exclude strings of less than 2 characters
	filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
	return filtered_words

positive_examples = ['http://www.engadget.com/2012/11/16/htc-droid-dna-review/', 'http://www.engadget.com/2012/10/08/samsung-galaxy-note-ii-review/', 'http://www.engadget.com/2012/11/16/htc-desire-x-review/', 'http://www.engadget.com/2012/11/16/htc-desire-x-review/']
train_set = [(list(get_list_of_words_in_url),True) for link in positive_examples]
classifier = NaiveBayesClassifier.train(train_set)
print get_list_of_words_in_url('http://www.theverge.com/2012/11/28/3699112/the-verge-year-one-our-big-stories-august-2012-through-november-2012')