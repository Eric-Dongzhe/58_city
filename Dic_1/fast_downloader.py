# encoding: utf-8

import requests


import urlparse
import urllib2
import random
import time
from datetime import datetime, timedelta
import socket

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 0
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 0


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxy_list = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:
            # result was not loaded from cache so still need to download
            # self.throttle.wait(url)
            proxy_ip = random.choice(self.proxy_list) if self.proxy_list else None
            headers = {'User-agent': self.user_agent}
            result = self.download1(url, headers, proxy_ip=proxy_ip, num_retries=self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']

    def download1(self, url, headers, proxy_ip, num_retries, data=None):
        print 'requests Downloading:', url

        proxy = {'http': proxy_ip} if proxy_ip else None

        try:
            r = requests.get(url, headers=headers, proxies=proxy)
            html = r.content
            code = r.status_code
        except Exception as e:
            print 'Download error:', str(e) + url
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 < code < 600:
                    return self.download1(url, headers, proxy_ip, num_retries-1, data)
            else:
                code = None
        return {'html': html, 'code': code}


class Throttle:
    """通过间隔时间来限制对同一domain的下载
    """
    def __init__(self, delay):
        # 对每个domain的下载的间隔时间
        self.delay = delay
        # 对最近被请求过的domian打上时间戳
        self.domains = {}

    def wait(self, url):
        """Delay if have accessed this domain recently
        """
        domain = urlparse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # domain 最近已经被请求过，所以需要sleep
                time.sleep(sleep_secs)
        # 更新最新的请求时间
        self.domains[domain] = datetime.now()
