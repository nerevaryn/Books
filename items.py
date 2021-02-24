# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    upc = scrapy.Field()
    availability = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    results_amount = scrapy.Field()
