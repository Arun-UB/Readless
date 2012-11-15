from bs4 import BeautifulSoup
import urllib
import re, argparse, sys
import string

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
    print (word_list) #only for testing
    return(word_list)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Accepts a URL")
    parser.add_argument("--url",dest = "url") #Extracts url from command line, if available
    urls = parser.parse_args()
    if urls.url == None:
        print ("No URL Specified")
        sys.exit()
    strip_html(urls.url)
