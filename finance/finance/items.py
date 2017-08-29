# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ReplyItem(scrapy.Item):

    authorurl = scrapy.Field()
    floornum = scrapy.Field()
    host = scrapy.Field()
    domain = scrapy.Field()
    bankuaiid = scrapy.Field()
    threadid = scrapy.Field()
    threadurl = scrapy.Field()
    tieziid = scrapy.Field()
    text = scrapy.Field()
    textquote = scrapy.Field()
    textorg = scrapy.Field()
    title = scrapy.Field()
    crawldate = scrapy.Field()
    sourceurl = scrapy.Field()
    bankuainame = scrapy.Field()
    authorname = scrapy.Field()
    publishdate = scrapy.Field()
    so = scrapy.Field(default='')

    tp = scrapy.Field()

    views = scrapy.Field()
    replies = scrapy.Field()
    likes = scrapy.Field()

    province = scrapy.Field()
    city = scrapy.Field()
    level = scrapy.Field()
    device = scrapy.Field()
    meta = scrapy.Field()

