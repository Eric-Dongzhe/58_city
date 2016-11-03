# -*- coding: utf-8 -*-

from thread_download import threaded_download
from html_cache import HtmlCache
from channel_extract import channels_list

channel = ['http://example.webscraping.com/index/',
           'http://tieba.baidu.com/f/index/forumpark?cn=%E5%8F%B0%E6%B9%BE%E7%94%B5%E5%BD%B1&ci=0&pcn=%E7%94%B5%E5%BD%B1&pci=0&ct=1&rn=20&pn=']

def main():
    # scrape_callback = AlexaCallback()
    html_cache = HtmlCache('ChannelPage_Cache')
    # cache.clear()
    channels_for_crawl = channel

    threaded_download(channels_for_crawl, cache=html_cache)


if __name__ == '__main__':

    main()
