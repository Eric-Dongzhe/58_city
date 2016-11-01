try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.binary import Binary


class UrlCache:
    """
    Wrapper around MongoDB to cache downloads

    >>> cache = MongoCache()
    >>> cache.clear()
    >>> url = 'http://example.webscraping.com'
    >>> result = {'html': '...'}
    >>> cache[url] = result
    >>> cache[url]['html'] == result['html']
    True
    >>> cache = MongoCache(expires=timedelta())
    >>> cache[url] = result
    >>> # every 60 seconds is purged http://docs.mongodb.org/manual/core/index-ttl/
    >>> import time; time.sleep(60)
    >>> cache[url]
    Traceback (most recent call last):
     ...
    KeyError: 'http://example.webscraping.com does not exist'
    """

    def __init__(self, tab_name, client=None, expires=timedelta(minutes=60)):

        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db_url = self.client.url_cache
        self.tab_name = tab_name
        self.db_url[self.tab_name].create_index('timestamp', expireAfterSeconds=expires.total_seconds())

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
        record = self.db_url[self.tab_name].find_one({'_id': url})
        if record:
            return record['result']
            # return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' does not exist')

    def setitem(self, url, name):
        """Save value for this URL
        """
        record = {'result': name, 'timestamp': datetime.utcnow()}
        # record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db_url[self.tab_name].update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db_url[self.tab_name].drop()
