from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html_data = BeautifulSoup(urlopen("http://www.instapaper.com/m?u=http%3A%2F%2Fwww.theverge.com%2F2012%2F10%2F23%2F3544788%2Fapple-ipad-mini-pricing-lower-cost-tablet").read())
html_data = html_data.find('body')

anchors = html_data.findAll('a')
for anchor in anchors:
	anchor.extract()

raw = re.sub('[\n\r"\t|“,”◆]','',html_data.get_text())

print (raw)
