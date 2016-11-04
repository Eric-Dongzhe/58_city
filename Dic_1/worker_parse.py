# -*- coding: utf-8 -*-


from process_parse import process_parse
from mongo_parse_queue import MongoParseQueue
from store import MongoStore
from mongo_download_queue import MongoDownloadQueue


def main():

    channel_page_parse_queue = MongoParseQueue('ChPage_Parse_Queue')
    data_store = MongoStore('Item_Result_Data')
    item_page_download_queue = MongoDownloadQueue('IPage_Download_Queue')
    while True:
        if channel_page_parse_queue:
            process_parse(parse_queue=channel_page_parse_queue, store=data_store, queue_to_put=item_page_download_queue)


if __name__ == '__main__':

    main()
