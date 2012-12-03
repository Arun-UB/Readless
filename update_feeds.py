from bs4 import BeautifulSoup
import urllib
import re, argparse, sys
import nltk
import feedparser
import pickle
from server import Article, Feed, Reader, User, Features, db
from dateutil.parser import parse
import re

pattern = re.compile('[\W_ ]+')



if __name__ == '__main__':
    update()