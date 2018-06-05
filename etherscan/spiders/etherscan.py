from scrapy import Spider
from scrapy import Request
import re
from ..items import EtherscanItem
from datetime import datetime
import time
from selenium import webdriver


class Etherscan(Spider):
    name = 'weibo'
    driver = None
    page = 1

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)

        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options = chrome_options)

    def start_requests(self):
        urls = [
            "https://weibo.com/u/5941645212",
        ]

        for url in urls:
            request = Request(url = url, callback = self.parse)
            yield request


    def parse(self, response):
        picture_url = response.xpath('//div[@class="con-1 hv-pos"]/img/@src').extract()
        video_timelength = response.xpath('//div[@class="con-4"]/div[@class="opt hv-pos hv-center"]/div[@class="opt-8"]/text()').extract()
        video_title = response.xpath('//a[@title="Bitangel宝二爷的秒拍视频"]/parent::div[@class="WB_text W_f14"]/text()').extract()
        video_jumpurl = response.xpath('//a[@title="Bitangel宝二爷的秒拍视频"]/@href').extract()

        if len(video_title) != 0:
            txt = True
            while txt:
                for i,l in enumerate(video_title):
                    if l.find(" \u200b\u200b\u200b\u200b") == 0 or l.find(" ") == 0:
                        del video_title[i]
                        txt = True
                        break
                    else:
                        txt = False

            txt = True
            while txt:
                for i,l in enumerate(video_title):
                    if l.find("\n") != 0 and i != 0:
                        video_title[i - 1] = video_title[i - 1] + l
                        del video_title[i]
                        txt = True
                        break
                    else:
                        txt = False

        for i in video_jumpurl:
            yield Request(url = i, callback = self.video_parse)

        print("#"*70)
        print(len(video_title))
        print(len(video_jumpurl))
        print(len(picture_url))
        print(len(video_timelength))
        print("#"*70)


    def video_parse(self, response):
        tmp = response.xpath('//div[@class="con-2 hv-pos hv-center"]/video/@src').extract()
        print("-"*70)
        print(tmp)


    @staticmethod
    def close(spider, reason):
        spider.driver.quit()
        return super().close(spider, reason)
