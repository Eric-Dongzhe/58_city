# -*- coding: utf-8 -*-

from thread_download import threaded_download
from html_cache import HtmlCache
from channel_extract import channels_list

channel_string = """http://nj.58.com//iphonesj/
http://nj.58.com//sanxing/
http://nj.58.com//nuojiya/
http://nj.58.com//htc/
http://nj.58.com//xiaomi/
http://nj.58.com//ailixin/
http://nj.58.com//zhongxingshouji/
http://nj.58.com//lgsj/
http://nj.58.com//kupaisj/
http://nj.58.com//huaweisj/
http://nj.58.com//lianxiang/
http://nj.58.com//motuoluola/
http://nj.58.com//heimei/
http://nj.58.com//jinlisj/
http://nj.58.com//meizu/
"""

# 选择 [Channels]
channel = channel_string.split()[0:1]


def main():

    html_cache = HtmlCache('ChPage_Cache')
    channels_for_crawl = channel

    threaded_download(channels_for_crawl, cache=html_cache)

    # channel_page_parse_queue = MongoParseQueue('channel_page_parse_queue')
    # data_store = MongoStore('Item_Result_Data')
    # item_page_download_queue = MongoDownloadQueue('item_page_download_queue')
    # process_parse(parse_queue=channel_page_parse_queue, store=data_store, queue_to_put=item_page_download_queue)


if __name__ == '__main__':

    main()
