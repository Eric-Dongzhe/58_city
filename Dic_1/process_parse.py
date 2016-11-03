# encoding: utf-8

import time
import threading
import urlparse
from mongo_parse_queue import MongoParseQueue
from mongo_download_queue import MongoDownloadQueue
from parser import ChannelPageParser

SLEEP_TIME = 1


def threaded_parse(seed_url, delay=5, cache=None, user_agent='wswp', proxies=None, num_retries=2, max_threads=2, timeout=10):
    """Crawl this website in multiple threads
    """
    # the queue of URL's that still need to be crawled
    channel_page_download_queue = MongoDownloadQueue('Ch_PageDownload_Queue')
    channel_page_download_queue.clear()
    channel_page_download_queue.push(seed_url)
    # downloader = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    channel_page_parse_queue = MongoParseQueue('Ch_Page_P_Queue')

    def process_queue():
        while True:
            try:
                channel_page_html = channel_page_parse_queue.pop()
                print 'pooooped'
            except KeyError:
                # crawl queue is empty
                break
            else:
                channel_page_parser = ChannelPageParser(channel_page_html)
                items_url = channel_page_parser()
                items_simple_data = channel_page_parser.get_data()
                if items_url:
                    item_page_parse_queue.push(page_url, html)
                channel_page_download_queue.complete(channel_url)
                """
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print 'Error in callback for: {}: {}'.format(url, e)
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            # check whether already crawled this link
                            if link not in seen:
                                seen.add(link)
                                # add this new link to queue
                                crawl_queue.append(link)
                """

    # wait for all download threads to finish
    threads = []
    while threads or channel_page_download_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and channel_page_download_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            print 'building threads'
            thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)
