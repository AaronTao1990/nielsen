import logging
import random
from utils.netcall import fetch_html
import re
import random
import base64

class ProxyManager(object):

    good_proxys = {}

    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def check_proxy(self):
        self.logger.info('proxys size : %d' % len(self.good_proxys))
        def get_new_ips():
            ips = []
            api = 'http://api.zdaye.com/?api=201605051157596943&pw=123&checktime=1%D0%A1%CA%B1%C4%DA&gb=2'
            resp = fetch_html(api)
            try:
                for line in resp.split('\n'):
                    ips.append('http://' + line.strip('\r'))
                return ips
            except Exception:
                return ips
        for i in range(5):
            if len(self.good_proxys) < 30:
                ips = get_new_ips()
                for ip in ips:
                    if ip in self.good_proxys.keys():
                        continue
                    else:
                        self.good_proxys[ip] = 0
            else:
                break

    def get_proxy(self):
        self.check_proxy()
        for i in range(30):
            proxy = random.choice(self.good_proxys.keys())
            if self.good_proxys[proxy] > 0:
                del self.good_proxys[proxy]
            else:
                return proxy

    def feed_back(self, proxy):
        self.logger.info('trying to del proxy : %s' % proxy)
        del self.good_proxys[proxy]

class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_manager = ProxyManager()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return

        proxy_address = self.proxy_manager.get_proxy()

        request.meta['proxy'] = proxy_address

    def process_exception(self, request, exception, spider):
        proxy = request.meta.get('proxy')
        if not proxy:
            spider.logger.error('invalid proxy')
            return
        try:
            self.proxy_manager.feed_back(proxy)
        except ValueError:
            pass
