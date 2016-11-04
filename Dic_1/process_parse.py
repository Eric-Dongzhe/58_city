# encoding: utf-8


import multiprocessing

from mongo_parse_queue import MongoParseQueue
from mongo_download_queue import MongoDownloadQueue
from my_parser import ChannelPageParser


def parse(parse_queue=None, store=None, queue_to_put=None):
    """Crawl this website in multiple threads
    """
    # the queue of URL's that still need to be crawled
    # channel_page_download_queue.clear()
    # channel_page_parse_queue = MongoParseQueue('Ch_Page_P_Queue')

    while True:
        try:
            channel_page = parse_queue.pop()
        except KeyError:
            # crawl queue is empty
            break
        else:
            channel_page_parser = ChannelPageParser(channel_page[1])
            items_url = channel_page_parser()
            items_simple_data = channel_page_parser.get_data()
            for url in items_url:
                if url:
                    queue_to_put.push(url)
            if store:
                store(items_url, items_simple_data)
            parse_queue.complete(channel_page[0])


def process_parse(**kwargs):
    # channel_page_parse_queue = MongoParseQueue('Ch_Page_P_Queue')
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print 'Starting {} processes'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=parse, kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()

