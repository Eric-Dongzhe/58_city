# encoding: utf-8

import urlparse
from bs4 import BeautifulSoup

from datetime import datetime, timedelta


DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 0
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 0

class ChannelPageParser:
    def __init__(self, html):
        socket.setdefaulttimeout(timeout)
        self.html = html
        self.cache = cache

    def __call__(self, html):
        soup = BeautifulSoup(html.text, 'lxml')
        try:
            item_url = soup.find('li', class_="next").find(href=re.compile(r"/page/"))
        except:
            return None
        return urlparse.urljoin(page_url, item_url['href'])

    def get_data(url, html):
        # return a list cotains dics
        # parse the soup, find all set of items in dic ways and put these dics in a list
        soup = BeautifulSoup(html.text, 'lxml')
        result = []
        title_nodes = soup.select('div.property_title > a')
        img_nodes = soup.select('img[width="160"]')
        tags_nodes = soup.select('div.p13n_reasoning_v2')

        for title, img, link, tag in zip(title_nodes, img_nodes, tags_nodes):
            # put these datas in a dic respectly
            res_data = {'title': title.get_text(),
                        'img': img.get_text(),
                        'about_link': urlparse.urljoin(url, link['href']),
                        'tag': list(tag.stripped_strings)}
            result.append(res_data)
        return result



class Parser:
    def __init__(self):

    def parse(self, html):
        data = {}
        return data

    def get_data(self):
        return data

    def get_link(self, data):

        return data['link'] if data['link'] else None


class LinkParser:
    def __init__(self):



    def get_link(self, html):

        return links


