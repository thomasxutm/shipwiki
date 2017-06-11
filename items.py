# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChuanbobaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Baikeitems(scrapy.Item):
    title = scrapy.Field()
#    content = scrapy.Field()
    tag = scrapy.Field()
    view_num = scrapy.Field()
    edit_time = scrapy.Field()
    edit_num = scrapy.Field()
    url = scrapy.Field()