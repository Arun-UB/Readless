from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import re, argparse, sys

def strip_html(url):
    html_data = BeautifulSoup(urlopen("http://www.instapaper.com/m?%s" % urlencode({'u':url})).read())
    html_data = html_data.find('body')
    
    anchors = html_data.findAll('a')
    for anchor in anchors:
        	anchor.extract()

    raw = re.sub('[\n\r"\t|,]','',html_data.get_text())

    print (raw)
	#return (raw)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Accepts a URL")
    parser.add_argument("--url",dest = "url")
    urls = parser.parse_args()
    if urls.url == None:
        print ("No URL Specified")
        sys.exit()
    strip_html(urls.url)
