from bs4 import BeautifulSoup
import urllib
import re, argparse, sys
import string

def strip_html(url):
    html_data = BeautifulSoup(urllib.urlopen("http://www.instapaper.com/m?%s" % urllib.urlencode({'u':url})).read())
    html_data = html_data.find("body")
    pattern = re.compile('[\W_ ]+')    
    words = html_data.findAll(text=True)
    word_list = []
    for word in words[13:]:
	for w in word.split(" "):
	    wd = (pattern.sub('',w.lower()))
	    if len(wd) > 1: word_list.append(wd)


    print (word_list)
    return(word_list)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Accepts a URL")
    parser.add_argument("--url",dest = "url")
    urls = parser.parse_args()
    if urls.url == None:
        print ("No URL Specified")
        sys.exit()
    strip_html(urls.url)
