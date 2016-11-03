from datetime import datetime, timedelta
from pymongo import MongoClient, errors


class MongoParseQueue:
    """
    >>> timeout = 1
    >>> url = 'http://example.webscraping.com'
    >>> q = MongoQueue(timeout=timeout)
    >>> q.clear() # ensure empty queue
    >>> q.push(url) # add test URL
    >>> q.peek() == q.pop() == url # pop back this URL
    True
    >>> q.repair() # immediate repair will do nothin
    >>> q.pop() # another pop should be empty
    >>> q.peek()
    >>> import time; time.sleep(timeout) # wait for timeout
    >>> q.repair() # now repair will release URL
    Released: test
    >>> q.pop() == url # pop URL again
    True
    >>> bool(q) # queue is still active while outstanding
    True
    >>> q.complete(url) # complete this URL
    >>> bool(q) # queue is not complete
    False
    """

    # possible states of a download
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, queue_tab_name, client=None, timeout=300):
        """
        host: the host to connect to MongoDB
        port: the port to connect to MongoDB
        timeout: the number of seconds to allow for a timeout
        """
        self.client = MongoClient() if client is None else client
        self.db_cache = self.client.parse_queue_db  # set the db using for queue
        self.queue_tab = self.db_cache[queue_tab_name]
        self.timeout = timeout

    def __nonzero__(self):
        """Returns True if there are more jobs to process
        """
        record = self.queue_tab.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url, html):
        """Add new URL to queue if does not exist
        """
        try:
            self.queue_tab.insert({'_id': url, 'html': html, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass  # this is already in the queue

    def pop(self):
        """Get an outstanding URL from the queue and set its status to processing.
        If the queue is empty a KeyError exception is raised.
        """
        record = self.queue_tab.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['html']
        else:
            self.repair()
            raise KeyError()

    def peek(self):
        record = self.queue_tab.find_one({'status': self.OUTSTANDING})
        if record:
            return record['html']

    def complete(self, url):
        """the url has been processed, and set the status flag to COMPLETE"""
        self.queue_tab.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """Release stalled jobs
        """
        record = self.queue_tab.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print 'Released:', record['html']

    def clear(self):
        self.queue_tab.drop()
