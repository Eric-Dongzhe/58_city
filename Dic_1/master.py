# -*- coding: utf-8 -*-

from link_crawler import link_crawler
from url_cache import UrlCache
from channel_extract import channels_list


def main():
    scrape_callback = channels_list
    cache = UrlCache('channels_url')
    # cache.clear()
    # process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, timeout=10, ignore_robots=True)
    link_crawler(None, scrape_callback=scrape_callback, cache=cache, timeout=10, ignore_robots=True)

if __name__ == '__main__':
    main()




