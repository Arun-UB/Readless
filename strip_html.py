from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import re

html_data = BeautifulSoup(urlopen("http://www.instapaper.com/m?%s" % urlencode({'u':'http://www.theverge.com/2012/10/23/3540550/microsoft-surface-review'})).read())
html_data = html_data.find('body')

anchors = html_data.findAll('a')
for anchor in anchors:
	anchor.extract()

raw = re.sub('[\n\r"\t|“,”◆]','',html_data.get_text())

print (raw)
