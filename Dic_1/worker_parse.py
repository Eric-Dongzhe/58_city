# -*- coding: utf-8 -*-

import time
from process_parse import process_parse
from mongo_parse_queue import MongoParseQueue
from store import MongoStore
from mongo_download_queue import MongoDownloadQueue


def main(wait=True):

    channel_page_parse_queue = MongoParseQueue('ChPage_Parse_Queue')
    # data_store = MongoStore('Item_Result_Data')
    # item_page_download_queue = MongoDownloadQueue('IPage_Download_Queue')
    while wait or channel_page_parse_queue:
        if wait:
            print 'Waiting..........'
            time.sleep(3)
        if channel_page_parse_queue:
            process_parse()


if __name__ == '__main__':

    main()
