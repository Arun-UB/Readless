from server import db
import datetime

class Features(db.EmbeddedDocument):
    '''An embedded document that represents the features of an article'''
    title = db.StringField(required = True)
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
        '''Arguments : URL
           Function: Gets the article only version of the URL using Instapaper.
           Extracts the text in the artcile and removes any non AlphaNumeric characters in the text
           Returns a list of words in the article present in the URL.'''
        html_data = BeautifulSoup(urllib.urlopen(
                         "http://www.instapaper.com/m?%s" % urllib.urlencode({'u':self.source_url})).read()) #URLencoding the url to pass it to Instapaper
        html_data = html_data.find("body")          #Using only the contents in HTML <body> tag, avoides Javascript from being treated as text.
        pattern = re.compile('[\W_ ]+')             #Compile regex for alphanumeric characters and spaces(for multiword strings).
        words = html_data.findAll(text=True)        #setting text to True to extract only the text in the <body>
        word_list = []                              #Stores the list of words
        for word in words[30:]:                     #Removing redundant content from Instapaper Mobilizer headers
            for w in word.split(" "):               #splitting on spcae for multiword strings
                wd = (pattern.sub('',w.lower()))    #substituing non alphanumeric characters with ''
                if len(wd) > 1 : word_list.append(wd)#exclude strings of less than 2 characters
        filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
        return dict((word,True) for word in word_list)

    def get_words_in_title(self):
        "Get words in the title of an article"
        word_list = []
        for w in self.features.title.split(" "):
            wd = (pattern.sub('',w.lower()))    
            if len(wd) > 1 : word_list.append(wd)
        filtered_words = [w for w in word_list if not w in nltk.corpus.stopwords.words('english')]
        return dict((word,True) for word in filtered_words)

    def get_score(self,classifier_object, article_features):
        "Use the trained classifier to find the interest for the new article"
        if classifier_object is None:
            return 0.5
        classifier = pickle.loads(classifier_object)
        if classifier.classify(get_words_in_title(article_features.title)) is True:
            return 1
        else:
            return 0

    def get_article_snippet(self,article, char_length = 128):
        '''
        Returns the article snippet to be show next to the article title.
        '''
        if(type(char_length) is int):                       #Make sure char_length a int parameter.
            html_data = BeautifulSoup(article)                          
            pattern = re.compile('[\W_ ]+')
            words = ''.join(html_data.findAll(text=True))   #Join the words from the html content.
            if len(article) < char_length:                  #Return the unedited snippet if length is less than the requested characters.
                return words + '...' 
            else:
                return words[:char_length] + '...'