# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from chuanbobaike.items import Baikeitems


class BaikespiderSpider(scrapy.Spider):
    name = 'baikespider'
    allowed_domains = ['http://wiki.eworldship.com/']
#    start_urls = ['http://wiki.eworldship.com/index.php?category-view-37-1/']

    def start_requests(self):
        # maxnum = response.xpath('//*[@id="fenye"]/a[11]/text()').extract()[0]
        # match_max = re.match(".*?(\d+).*", maxnum)
        # if match_max:
        #     maxnum = match_max.group(1)
        list = [37,38,39,41,36]
        bashurl = 'http://wiki.eworldship.com/index.php?category-view-'
        for i in list:
            url = bashurl + str(i) +'-1'
            yield Request(url, self.parse_page, dont_filter=True)

    def parse_page(self, response):
        maxnum = response.xpath('//*[@id="fenye"]/a[11]/text()').extract()[0]
        match_max = re.match(".*?(\d+).*", maxnum)
        bashurl = str(response.url)[:-2]
        if match_max:
            maxnum = match_max.group(1)
        for i in range(1, 5):
            url = bashurl + '-'+ str(i)
            yield Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="html"]/body/div[3]/dl/dt/a')
        for post_node in post_nodes:
                # img_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            newurl = parse.urljoin(response.url, post_url)
            yield Request(url=newurl, callback=self.parse_detail, dont_filter=True)




    def parse_detail(self, response):
        Baike = Baikeitems()
        title = response.css(".title_thema span::text").extract()[0]
        tag = response.css(".title_thema span::text").extract()[0]
        content = response.xpath("/html/body/div[3]/div[3]").extract()[0]
        #post_url = response.xpath('//*[@id="html"]/body/div[3]/dl/dt/a/@href').extract()
        view_num = response.xpath('//*[@id="html"]/body/div[4]/div[2]/ul/li[1]/text()').extract()[0]
        match_view = re.match(".*?(\d+).*", view_num)
        if match_view:
            view_num = match_view.group(1)
        else:
            view_num = 0
        edit_num = response.xpath('//*[@id="html"]/body/div[4]/div[2]/ul/li[2]/text()').extract()[0]
        match_edit = re.match(".*?(\d+).*", edit_num)
        if match_view:
            edit_num = match_edit.group(1)
        else:
            edit_num = 0
        edit_time = response.xpath('//*[@id="html"]/body/div[4]/div[2]/ul/li/text()').extract()
        for i in edit_time:
            match_time = re.match(".*?(\d+[-]\d+[-]\d+).*", i)
            if match_time:
                edit_time = match_time.group(1)
            else:
                edit_time = 0
        Baike["title"] = title
        Baike["url"] = response.url
        Baike["tag"] = tag
        Baike["edit_time"] = edit_time
        Baike["view_num"] = view_num
#        Baike["content"] = content
        Baike["edit_num"] = edit_num
        yield Baike
