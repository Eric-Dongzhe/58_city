try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.binary import Binary


class HtmlCache:
    """
    Wrapper around MongoDB to cache downloaded html

    >>> cache = HtmlCache('channels_link', client=client, exp_time=7(days), compress=False)
    >>> cache.clear()
    >>> url = 'http://example.webscraping.com/channel_page/'
            'http://example.webscraping.com/item_page/'
    >>> result = {'html': '...'}
    >>> cache.setitem(url,result)
    >>> cache.getitem(url) == result['html']
    True
    >>> cache = HtmlCache(exp_time=1seconds)
    >>> cache.setitem(url, result)
    >>> # every 60 seconds is purged http://docs.mongodb.org/manual/core/index-ttl/
    >>> import time; time.sleep(60)
    >>> cache.getitem(url)
    Traceback (most recent call last):
     ...
    KeyError: 'http://example.webscraping.com does not exist'
    """

    def __init__(self, tab_name, client=None, exp_time=7, compress=False):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db_html = self.client.html_cache
        self.tab_name = tab_name
        expires = timedelta(days=exp_time)
        self.db_html[self.tab_name].create_index('timestamp', expireAfterSeconds=expires.total_seconds())
        self.compress = compress

    def contains(self, url):
        try:
            self.getitem(url)
        except KeyError:
            return False
        else:
            return True

    def getitem(self, url):
        """Load value at this URL
        """
        record = self.db_html[self.tab_name].find_one({'_id': url})
        if record:
            if self.compress:
                return pickle.loads(zlib.decompress(record['result']))
            else:
                return record['result']
        else:
            raise KeyError(url + ' does not exist')

    def setitem(self, url, result):
        """Save value for this URL
        """
        if self.compress:
            record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        else:
            record = {'result': result, 'timestamp': datetime.utcnow()}

        self.db_html[self.tab_name].update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db_html[self.tab_name].drop()
