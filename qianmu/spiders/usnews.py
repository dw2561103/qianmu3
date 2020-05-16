# -*- coding: utf-8 -*-
import scrapy


class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['www.qianmu.org']
    start_urls = ['http://www.qianmu.org/ranking/1528.htm']

    def parse(self, response):
        links = response.xpath('//div[@class="rankItem"]//tr[position()>1]/td[2]/a/@href').extract()
        for link in links:
            yield response.follow(link, self.parse_univerity)

    def parse_univerity(self, response):
        data = {}
        data['name'] = response.xpath('//div[@id="wikiContent"]/h1/text()').extract_first()
        col1s = response.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//td[1]').extract()
        col2s = response.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//td[2]').extract()
        keys = [''.join(col.xpath('.//text()').extract_first()) for col in col1s]
        values = [''.join(col.xpath('.//text()').extract_first()) for col in col2s]
        if len(keys) == len(values):
            data.update(zip(keys, values))
        yield data
