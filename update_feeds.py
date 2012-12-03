from bs4 import BeautifulSoup

import re, argparse, sys
import nltk
import feedparser

from server import Article, Feed, Reader, User, Features, db

import re

pattern = re.compile('[\W_ ]+')



if __name__ == '__main__':
    update()