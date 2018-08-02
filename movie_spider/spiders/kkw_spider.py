import scrapy
import sys
import re
from movie_spider.items import MovieSpiderItem

reload(sys)
sys.setdefaultencoding('utf-8')


class QuotesSpider(scrapy.Spider):
    name = "kkw"
    base_url = 'http://www.kankanwu.com'
    start_urls = [
        base_url,
    ]

    def parse(self, response):

        items = []

        categorys = response.css(
            'div#header>div#navbar>div.layout>ul#nav>li.nav-item')

        for i in range(1, len(categorys) - 1):
            item = MovieSpiderItem()
            item['category'] = categorys[i].css(
                'a.nav-link::text').extract_first()
            item['category_url'] = type(
                self).base_url + categorys[i].css('a.nav-link::attr(href)').extract_first()
            items.append(item)

        for item in items:
            # self.logger.info(item)
            yield scrapy.http.Request(
                url=item['category_url'], meta={'category': item}, callback=self.sub_category_parse)
            # break

    def sub_category_parse(self, response):

        items = []

        category = response.meta['category']

        sub_categorys = response.css(
            'div#channel-nav>div.layout>ul.channel-catalog>li')

        if (len(sub_categorys) > 0):
            for i in range(0, len(sub_categorys) - 1):
                item = MovieSpiderItem()
                item['category'] = category['category']
                item['category_url'] = category['category_url']

                item['sub_category'] = sub_categorys[
                    i].css('a::text').extract_first()
                item['sub_category_url'] = sub_categorys[
                    i].css('a::attr(href)').extract_first()
                items.append(item)
        else:
            item = MovieSpiderItem()
            item['category'] = category['category']
            item['category_url'] = category['category_url']

            item['sub_category'] = category['category']
            item['sub_category_url'] = category['category_url']
            items.append(item)

        for item in items:
            yield scrapy.http.Request(
                url=item['sub_category_url'], meta={'sub_category': item}, callback=self.movie_parse)
            # break
            # self.logger.info(item)

    def movie_parse(self, response):

        items = []

        sub_category = response.meta['sub_category']

        movies = response.css(
            'div#content>div#letter-focus>dl.letter-focus-item>dd')

        for i in range(0, len(movies) - 1):
            item = MovieSpiderItem()
            item['category'] = sub_category['category']
            item['category_url'] = sub_category['category_url']
            item['sub_category'] = sub_category['sub_category']
            item['sub_category_url'] = sub_category['sub_category_url']

            item['title'] = movies[i].css('a::text').extract_first()
            item['url'] = type(self).base_url + \
                movies[i].css('a::attr(href)').extract_first()
            items.append(item)

        for item in items:
            yield scrapy.http.Request(url=item['url'], meta={'item':
                                                             item}, callback=self.movie_detail_parse)
            # self.logger.info(item)
            # break

        # self.logger.info(item)

    def movie_detail_parse(self, response):
        item = response.meta['item']

        detail_cols = response.css('div#content>div#detail-box>div.detail-cols')
        item['img_url'] = detail_cols.css('div.detail-pic>img::attr(src)').extract_first()
        detail_infos = detail_cols.css('div.detail-info>div.info>dl')

        item['actors'] = []
        for actor in detail_infos[0].css('dd>a::text').extract():
            item['actors'].append(actor)

        item['state'] = detail_infos[1].css('dd>span::text').extract_first()

        item['styles'] = []
        for style in detail_infos[2].css('dd>a::text').extract():
            item['styles'].append(style)

        item['district'] = detail_infos[3].css('dd>span>a::text').extract_first()

        item['language'] = detail_infos[4].css('dd>span::text').extract_first()

        item['director'] = detail_infos[5].css('dd>a::text').extract_first()

        item['date'] = detail_infos[6].css('dd>span::text').extract_first()

        item['year'] = detail_infos[7].css('dd>span::text').extract_first()

        item['description'] = detail_infos[9].css('dd::text').extract_first()

        play_list = response.css('div#content>div#detail-list>div.play-list-box>div.content>p.play-list>a')
        item['episode_titles'] = []
        item['episode_page_urls'] = []
        item['episode_urls'] = []
        for play in play_list:
            item['episode_titles'].append(play.css('::text').extract_first())
            item['episode_page_urls'].append(type(self).base_url + play.css('::attr(href)').extract_first())
            item['episode_urls'].append('')

        for i in range(0, len(item['episode_page_urls'])):
            page_url = item['episode_page_urls'][i]
            yield scrapy.http.Request(url=page_url, meta={'item':
                                                          item, 'index': i}, callback=self.movie_play_url_parse)

        # self.logger.info(item)

    def movie_play_url_parse(self, response):
        item = response.meta['item']
        index = response.meta['index']
        item['episode_urls'][index] = re.match('.*\?id=(.*)', response.css('iframe::attr(src)').extract_first(), 0).group(1)
        isFinish = True
        for url in item['episode_urls']:
            if url == '':
                isFinish = False
                break

        if isFinish:
            # self.logger.info(item)
            yield item
