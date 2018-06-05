from scrapy import Spider
from scrapy import Request
import re
from ..items import EtherscanItem
from datetime import datetime
import time
from selenium import webdriver


class Etherscan(Spider):
    name = 'youku'
    driver = None
    page = 1

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)

        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options = chrome_options)

    def start_requests(self):
        url = "http://so.youku.com/search_video/q_%E4%BB%A5%E5%A4%AA%E5%9D%8A?spm=a2h0k.11417342.pageturning.dpagenumber&pg="

        for i in range(1, 2):
            request = Request(url = url + str(i), callback = self.parse)
            js = "var q=document.documentElement.scrollTop="
            for i in range(1, 1000):
                self.driver.execute_script(js + str(i))
            yield request


    def parse(self, response):
        #移动滚轮加载图片数据

        #video_point = self.driver.find_elements_by_xpath('//div[@class="sk-mod"]')
        js = "var q=document.documentElement.scrollTop="
        for i in range(1, 1000):
            self.driver.execute_script(js + str(i))
        #    self.driver.execute_script("arguments[0].scrollIntoView();", i) #拖动到可见的元素去
        #self.driver.execute_script(js)

        video_title_list = response.xpath('//div[@class="sk-mod"]/div[@class="mod-main"]/div[@class="mod-header"]/h2[@class="spc-lv-1"]/a[@target="_blank"]').extract()
        picture_url_list = response.xpath('//div[@class="sk-mod"]/div[@class="mod-left"]/a[@class="sk-pack"]/div[@class="pack-cover"]/img/@src').extract()
        video_jumpurl_list = response.xpath('//div[@class="sk-mod"]/div[@class="mod-left"]/a[@class="sk-pack"]/@href').extract()
        video_uploadtime_list = response.xpath('//div[@class="sk-mod"]/div[@class="mod-main"]/div[@class="mod-info"]/p/span[1]/text()').extract()
        video_timelength_list = response.xpath('//div[@class="sk-mod"]/div[@class="mod-left"]/a[@class="sk-pack"]/span[@class="pack-rb pack-time"]/text()').extract()


        for i in range(0, len(video_title_list)):
            #上传时间变成时间戳格式
            time_str = ""
            time_list = video_uploadtime_list[i].split("-")
            if len(time_list[1]) == 1:
                time_str += time_list[0] + "-0" + time_list[1]
            else:
                time_str += time_list[0] + "-" + time_list[1]

            if len(time_list[2]) == 1:
                time_str += "-0" + time_list[2]
            else:
                time_str += "-" + time_list[2]
            
            time_int = int(time.mktime(time.strptime(time_str, "%Y-%m-%d ")))

            #视频框链接
            video_id = video_jumpurl_list[i].split('_')
            video_url = "http://player.youku.com/embed/" + video_id[-1][:-5]

            #标题整合
            video_title = ""
            str_html = video_title_list[i][video_title_list[i].find(">") + 1: -4]
            texts = str_html.split("<em class=\"hl\">")
            for l in texts:
                for t in l.split("</em>"):
                    video_title += t

            #将视频长度转换为秒数
            video_length = 0
            if len(video_timelength_list[i]) == 5:
                video_length = int(time.mktime(time.strptime("2010-01-01 00:" + video_timelength_list[i], "%Y-%m-%d %H:%M:%S"))) - int(time.mktime(time.strptime("2010-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
            else:
                video_length = int(time.mktime(time.strptime("2010-01-01 0" + video_timelength_list[i], "%Y-%m-%d %H:%M:%S"))) - int(time.mktime(time.strptime("2010-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
            
            
            print("-" * 70)
            #print({"video_length":video_length, "plays_num":0, "video_title":video_title, "video_createtime":int(time.time()),\
            #"video_timelength":video_timelength_list[i], "video_url":video_url, "picture_url":"http:" + picture_url_list[i],\
            #"video_uploadtime":time_int, "video_jumpurl":"http:" + video_jumpurl_list[i], "video_type":"NULL"})
            print("http:" + picture_url_list[i])
            print(len(picture_url_list))

            
            #es入库
            #es.index(index="video", doc_type="document", body={"video_length":video_length,"plays_num":plays_num,"video_title":title,\
            #"video_createtime":time_now,"video_timelength":self.video_timelength[i],"video_url":video_url,"picture_url":self.picture_url[i],\
            #"video_uploadtime":time_int,"video_jumpurl":video_jumpurl,"video_type":"NULL"})
            
        print("-" * 70)


    @staticmethod
    def close(spider, reason):
        spider.driver.quit()
        return super().close(spider, reason)
