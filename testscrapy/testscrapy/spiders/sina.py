# -*- coding: UTF-8 -*-
import scrapy
import re
import time
import csv
from ..items import  LiveItem
from ..struct import Content,Question
from scrapy.http import Request
class SinaSpider(scrapy.Spider):
    name = "sina"
    parse_mode = "blogger"
    start_urls = ["http://live.finance.sina.com.cn"]
    data = []


    def parse(self, response):
        self.live_url_head = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_&s=program&a=ask_detail&format=json&uid=2132536197&askuid=&pagesize=100&isans=0&per="
        self.live_url_last = "&_="
        self.all_num = 0
        self.current_blogger = ''

        if (self.parse_mode == "blogger"):
            start_urls = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_1515759877729937&p=course&s=teacher&a=lists&format=json&extra=program%2Cfollow&page=1&pagesize=30&buid=&ordertype=1&_=1515758197511"
            self.url_head = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_1515759877729937&p=course&s=teacher&a=lists&format=json&extra=program%2Cfollow&page="
            self.url_last = "&pagesize=30&buid=&ordertype=1&_=1515758197511"
            self.live_url_head = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_&s=program&a=ask_detail&format=json&uid=2132536197&askuid=&pagesize=100&isans=0&per="
            self.live_url_last = "&_="
            self.url_num = 1
            self.id = []
            self.follow_num = []
            self.like_num = []
            self.view_num = []
            yield Request(start_urls, callback=self.parse_blogger)
            return


    def parse_live(self,response):
        current_blogger = response.meta['id']
        data = response.body
        text = data.decode('unicode_escape').replace('\\', '')
        text = text.replace('\n', ' ')
        items = LiveItem()
        blocks = re.findall(r"\"id\":(.+?)}", text)
        for block in blocks:
            time = re.findall(r"\"time\":(.+?),", block)
            content = re.findall(r"\"content\":\"(.+?)\",", block)
            items['id'] = current_blogger
            items['q_timestamp'] = self.time_translate(time[0])  # time[0]
            items['question'] = content[0]
            items['a_timestamp'] = (('' if len(time) == 1 else self.time_translate(time[1])))
            items['answer'] = ('' if len(content) == 1 else content[1])
            yield items
        id = re.findall(r"\"id\":\"(\d+?)\",\"uid", text)

        # check if it is the end
        if (len(id) == 0 or self.all_num > 300000):
            print("all numbers:", self.all_num)
            return
        else:
            self.all_num += len(id)
            next_url = self.live_url_head + id[-1] + self.live_url_last
            yield Request(next_url,meta={'id': current_blogger}, callback=self.parse_live)
            return





    def parse_blogger(self,response):
        data = response.body
        text = data.decode('unicode_escape').replace('\\','')
        blocks = re.findall(r"\"id\":\"(.+?)follow_status", text)
        for block  in blocks :
            if(block == ""):
                continue
            id_tem = re.findall(r"\"uid\":\"(\d+?)\",\"name", block)
            name = re.findall(r"\"name\":\"(.+?)\",", block)
            follow_num_tem = re.findall(r"\"follow_num\":(\d+?),", block)
            like_num_tem = re.findall(r"\"like_num\":\"(\d+?)\"", block)
            view_num_tem = re.findall(r"\"view_num\":\"(\d+?)\",\"col", block)
            signature = re.findall(r"\"signature_long\":\"(.+?)\"", block)
            self.id += id_tem
            self.data += [id_tem + name + follow_num_tem + like_num_tem + view_num_tem + signature]
        if(len(blocks) > 0):
            self.url_num += 1
            next_url = self.url_head + str(self.url_num) + self.url_last
            yield Request(next_url, callback=self.parse_blogger)
        else:
            csvfile = open('D:\SINA_BLOGGER.csv', 'w', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(['id','name','follow num', 'like num', 'view num', 'signature'])
            for data in self.data:
                writer.writerow(data)
            csvfile.close()
            for current_blogger in self.id:
                live_url= "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_&s=program&a=ask_detail&format=json&uid="+ current_blogger +"&askuid=&pagesize=100&isans=0&per=" + self.live_url_last
                yield Request(live_url, meta={'id': current_blogger}, callback=self.parse_live)

    def time_translate(self,timestamp):
        timestamp = int(timestamp)
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt;