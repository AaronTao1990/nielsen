
class RandomProxy(object):
    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        pass

    def process_exception(self, request, exception, spider):
        proxy = request.meta.get('proxy')
        if not proxy:
            spider.logger.error('invalid proxy')
            return
        try:
            spider.failed_proxy(proxy)
            spider.logger.error('try to remove proxy')
        except ValueError:
            pass
