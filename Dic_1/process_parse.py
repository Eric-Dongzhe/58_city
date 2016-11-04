# encoding: utf-8


import multiprocessing

from store import MongoStore
from mongo_parse_queue import MongoParseQueue
from mongo_download_queue import MongoDownloadQueue
from my_parser import ChannelPageParser


parse_queue_name = 'ChPage_Parse_Queue'
store_name = 'Item_Result_Data'
queue_to_put_name = 'IPage_Download_Queue'


def parse():
    """Crawl this website in multiple threads
    """
    parse_queue = MongoParseQueue(parse_queue_name)
    store = MongoStore(store_name)
    queue_to_put = MongoDownloadQueue(queue_to_put_name)
    while True:
        try:
            channel_page = parse_queue.pop()
        except KeyError:
            print 'crawl queue is empty'
            break
        else:
            channel_page_parser = ChannelPageParser(channel_page[1])

            items_url = channel_page_parser()
            items_simple_data = channel_page_parser.get_data()
            print items_simple_data
            if store:
                for url, item_data in zip(items_url, items_simple_data):
                    if url:
                        queue_to_put.push(url)
                    store[url] = item_data
            else:
                for url in items_url:
                    queue_to_put.push(url)
            # store[url] = items_simple_data
            # store(items_url, items_simple_data)
            parse_queue.complete(channel_page[0])


def process_parse():
    # channel_page_parse_queue = MongoParseQueue('ChPage_Parse_Queue')
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print 'Starting {} processes'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        # p = multiprocessing.Process(target=parse)
        p = multiprocessing.Process(target=parse)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
