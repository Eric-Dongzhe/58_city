#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
# from multiprocessing import Process, Queue
from Queue import Queue
import threading
import pymongo
import requests

from channel_extract import channels_string

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']  # Database
url_list = ceshi['url_list']  # Table url_list
items_data = ceshi['items_data']  # Table items_data

ExitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print "Starting " + self.name
        get_all_page_from(self.name, self.q)
        print "Exiting " + self.name


def download(channel, pages, who_sells=0):
    list_view = '{}{}/pn{}'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    return list_view


def put_url_to_queue(url_queue, channel__list):
    for channel in channel_list:
        url_queue.put(channel)
        print('put channel Link queue size is %d' % (url_queue.qsize(),))


def get_all_page_from(thread_name, queue):
    while not ExitFlag:
        # queueLock.acquire()
        if not Channel_Queue.empty():
            channel_for_parse = queue.get()
            # queueLock.release()
            for page in xrange(1, 30):
                channel_list_url = download(channel_for_parse, page)
                print "%s processing %s" % (thread_name, channel_list_url)
                # Log_thread.write("----%s processing %s----\n" % (threadName, channel_list))
        else:
            pass  # queueLock.release()
        # time.sleep(1)


if __name__ == '__main__':
    channel_list = channels_string.split()
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8"]
    Channel_Queue = Queue(10)
    queueLock = threading.Lock()
    threads = []
    threadID = 1

    # 创建新线程
    for tName in threadList:
        thread = MyThread(threadID, tName, Channel_Queue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for channel_url in channel_list:
        Channel_Queue.put(channel_url)
    queueLock.release()

    # 等待队列清空
    while not Channel_Queue.empty():
        pass

    # 通知线程是时候退出
    ExitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print "Exiting Main Thread"