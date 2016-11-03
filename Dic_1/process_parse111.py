# encoding: utf-8

import urlparse
from mongo_parse_queue import MongoParseQueue
from mongo_download_queue import MongoDownloadQueue
from parser import ChannelPageParser


def parse(store=None):
    """Crawl this website in multiple threads
    """
    # the queue of URL's that still need to be crawled
    channel_page_download_queue = MongoDownloadQueue('Ch_PageDownload_Queue')
    # channel_page_download_queue.clear()
    channel_page_download_queue.push(seed_url)
    # downloader = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    channel_page_parse_queue = MongoParseQueue('Ch_Page_P_Queue')

    while True:
        try:
            channel_page_html = channel_page_parse_queue.pop()
            # print 'pooooped'
        except KeyError:
            # crawl queue is empty
            break
        else:
            channel_page_parser = ChannelPageParser(channel_page_html)
            items_url = channel_page_parser()
            items_simple_data = channel_page_parser.get_data()
            if items_url:
                item_page_parse_queue.push(page_url, html)
            if store:
                store()
            channel_page_download_queue.complete(channel_url)


def process_parser(args, **kwargs):
    # channel_page_parse_queue = MongoParseQueue('Ch_Page_P_Queue')
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print 'Starting {} processes'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=parse, args=[args], kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()

