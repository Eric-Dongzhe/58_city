# encoding: utf-8

try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.binary import Binary









class MongoStore:
    """
    Wrapper around MongoDB to cache downloaded html

    >>> cache = HtmlCache('channels_link', client=client, exp_time=7(days), compress=False)
    >>> cache.clear()
    >>> url = 'http://example.webscraping.com/channel_page/'
            'http://example.webscraping.com/item_page/'
    >>> result = {'html': '...'}
    >>> cache[url] = result
    >>> cache[url]['html'] == result['html']
    True
    >>> cache = HtmlCache(exp_time=1)
    >>> cache[url] = result
    >>> # every 60 seconds is purged http://docs.mongodb.org/manual/core/index-ttl/
    >>> import time; time.sleep(60)
    >>> cache[url]
    Traceback (most recent call last):
     ...
    KeyError: 'http://example.webscraping.com does not exist'
    """
    def __init__(self, store_tab_name, client=None, compress=False):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db_html = self.client.DataStored
        self.store_tab = self.db_html[store_tab_name]
        # expires = timedelta(days=exp_time)
        # self.cache_tab.create_index('timestamp', expireAfterSeconds=expires.total_seconds())
        self.compress = compress

    def __contains__(self, url):
        """
        try:
            # self.getitem(url)
            self[url]
        except KeyError:
            return False
        else:
            return True
        """
        return True

    def __getitem__(self, url):
        """Load value at this URL
        """
        record = self.store_tab.find_one({'_id': url})
        if record:
            if self.compress:
                return pickle.loads(zlib.decompress(record['result']))
            else:
                return record['result']
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save value for this URL
        """
        if self.compress:
            record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        else:
            record = {'result': result, 'timestamp': datetime.utcnow()}

        self.store_tab.update({'_id': url}, {'$set': record}, upsert=True)

