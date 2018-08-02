# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    category = scrapy.Field()  # 电视剧、电影
    category_url = scrapy.Field()
    sub_category = scrapy.Field()  # 国产剧、香港剧、喜剧片、动作片
    sub_category_url = scrapy.Field()

    url = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    score = scrapy.Field()
    actors = scrapy.Field()
    state = scrapy.Field()
    styles = scrapy.Field()
    district = scrapy.Field()
    language = scrapy.Field()
    director = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    description = scrapy.Field()
    episode_page_urls = scrapy.Field()
    episode_titles = scrapy.Field()
    episode_urls = scrapy.Field()

    pass
