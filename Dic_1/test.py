# encoding: utf-8

from my_parser import ChannelPageParser
from bs4 import BeautifulSoup
import requests

class HtmlDownloader(object):
    """docstring for HemlDownloader"""

    def download(self, url):
        if url is None:
            return None
        '''
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
        return None
        '''

        # return response.read()
        print 'down %s', url
        return requests.get(url)

downloader = HtmlDownloader()
url = 'http://nj.58.com//iphonesj/'
html = downloader.download(url)

parser = ChannelPageParser(html)

