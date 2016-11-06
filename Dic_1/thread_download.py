# encoding: utf-8


import time
import threading
import urlparse
from mongo_parse_queue import MongoParseQueue
from mongo_download_queue import MongoDownloadQueue
# from downloader import Downloader
from fast_downloader import Downloader


SLEEP_TIME = 1


def threaded_download(seed_url, delay=5, cache=None, user_agent='wswp', proxies=None, num_retries=2, max_threads=8, timeout=10):
    """Crawl this website in multiple threads
    """
    # the queue of URL's that still need to be crawled
    channel_page_download_queue = MongoDownloadQueue('ChPage_Download_Queue')
    # channel_page_download_queue.clear()
    channel_page_download_queue.push(seed_url)
    downloader = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    channel_page_parse_queue = MongoParseQueue('ChPage_Parse_Queue')

    def process_queue():
        while True:
            try:
                channel_url = channel_page_download_queue.pop()

            except KeyError:
                # crawl queue is empty
                break
            else:
                for page_url in page_controller(channel=channel_url, page_num=20):  # get all pages of a channel
                    html = downloader(page_url)
                    if html:
                        channel_page_parse_queue.push(page_url, html)
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


def page_controller(channel, page_num):
    pages = []
    for page in range(1, page_num + 1):
        view_list = '{}pn{}'.format(channel, page)
        # view_list = urlparse.urljoin(channel, str(page))
        pages.append(view_list)
    return pages


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)
