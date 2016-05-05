# -*- coding: utf-8 -*-

# Scrapy settings for sogou_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sogou_crawler'

SPIDER_MODULES = ['sogou_crawler.spiders']
NEWSPIDER_MODULE = 'sogou_crawler.spiders'

CONCURRENT_REQUESTS = 60
DOWNLOAD_DELAY = 0.8
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOAD_TIMEOUT = 10

COOKIES_ENABLES=False

USE_PROXY = False

REDIS_CONFIG = {
    'host' : '172.31.18.41',
    'port' : 6379,
    #'host' : '10.111.0.12',
    #'port' : 6380,
    'ntasks' : 'qunar',
    'proxy' : 'proxy'
}

DOWNLOADER_MIDDLEWARES = {
    #'sogou_crawler.redirect_middleware.RedirectMiddleware' : 500,
    #'scrapy.downloadermiddlewares.cookies.CookiesMiddleware' : None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'sogou_crawler.middlewares.rotate_useragent.RotateUserAgentMiddleware' : 400
}
