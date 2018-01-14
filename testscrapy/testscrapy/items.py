# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiveItem(scrapy.Item):
    id = scrapy.Field()
    q_timestamp = scrapy.Field()
    question = scrapy.Field()
    a_timestamp = scrapy.Field()
    answer = scrapy.Field()
    pass



class BozhuItem(scrapy.Item):
    id = scrapy.Field()
    follow_num = scrapy.Field()
    like_num = scrapy.Field()
    view_num= scrapy.Field()
    pass


class THS_BLOG(scrapy.Item):
    id = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    pass

class THS_BLOGGER(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    like_num = scrapy.Field()
    newsNum = scrapy.Field()
    visitNum = scrapy.Field()
    pass