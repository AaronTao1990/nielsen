from scrapy.core.scheduler import Scheduler
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
import urllib
import json

class BaseScheduler(Scheduler):

    def get_next_request(self):
        pass

    def next_request(self):
        next_request = Scheduler.next_request(self)
        if next_request:
            return next_request

        # get next request
        for request in self.get_next_request():
            self.enqueue_request(request)

        next_request = Scheduler.next_request(self)
        if next_request:
            return next_request
        return next_request

    def ensure_utf8(self, s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

class NielsenScheduler(BaseScheduler):

    def get_next_request(self):
        task_str = self.spider.keywords_dao.get_tasks()
        self.spider.logger.info('task info : %s' % task_str)
        task = json.loads(task_str)
        meta = {
            'task' : task,
            'task_str' : task_str
        }
        yield Request(url=task['url'],
                      meta=meta,
                      headers=self.spider.HEADERS,
                      callback=self.spider.parse_api,
                    )


