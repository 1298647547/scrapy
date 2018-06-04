from scrapy import Spider
from scrapy import Request
import re
from ..items import EtherscanItem
from datetime import datetime
import time
from selenium import webdriver


class Etherscan(Spider):
    name = 'etherscan'
    driver = None
    page = 1

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def start_requests(self):
        urls = [
            "https://weibo.com/u/5941645212",
        ]

        for url in urls:
            self.logger.info('starting .....')
            request = Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        item = EtherscanItem()

        content = response.xpath('//*[@id="Pl_Official_MyProfileFeed__20"]/div/div[4]/div[1]/div[3]/div[4]').extract()
        print("#"*100)
        print(content)
        print("#"*100)

    @staticmethod
    def close(spider, reason):
        spider.driver.quit()
        return super().close(spider, reason)
