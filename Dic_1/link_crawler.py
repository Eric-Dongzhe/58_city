# -*- coding: utf-8 -*-

from html_cache import HtmlCache

from bs4 import BeautifulSoup


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            cache = HtmlCache('channel_page')
            soup = BeautifulSoup(html.txt, 'lxml')
            channel_links = soup.select()
            for channel in channel_links:
                urls.append(channel)

            with ZipFile(StringIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for _, website in csv.reader(zf.open(csv_filename)):
                    if 'http://' + website not in cache:
                        urls.append('http://' + website)
                        if len(urls) == self.max_urls:
                            break
            return urls
