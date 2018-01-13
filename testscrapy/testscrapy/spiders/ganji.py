# -*- coding: UTF-8 -*-
import scrapy
import re
import time
import csv
from ..items import  LiveItem
from ..struct import Content,Question
from scrapy.http import Request
class ganjispider(scrapy.Spider):
    name = "sina"
    parse_mode = "blogger"
    start_urls = ["http://live.finance.sina.com.cn"]
    data = []


    def parse(self, response):
        self.live_url_head = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_&s=program&a=ask_detail&format=json&uid=2132536197&askuid=&pagesize=100&isans=0&per="
        self.live_url_last = "&_="
        self.all_num = 0
        self.current_blogger = ''
        if(self.parse_mode == "homepage"):
            start_urls = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_1515823711844202&p=course&s=program&a=pic_live_detail&format=json&totalflag=1&uid=&program_id=&old=&per=&pagesize=20&_=1515823711829"
            self.url_head = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_1515823797811263&p=course&s=program&a=pic_live_detail&format=json&totalflag=1&uid=&program_id=&old=1&per="
            self.url_last = "&pagesize=2000&_=1515823711833"
            self.all_num = 0
            yield Request(start_urls, callback=self.parse_homepage)
            return
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
        if(self.parse_mode == "live"):
            start_urls = "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_1515828348289690&s=program&a=ask_detail&format=json&uid=2132536197&askuid=&pagesize=20&isans=0&per=&_=1515828325106"
            yield Request(start_urls, meta={'id': "0"},callback=self.parse_live)
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
            self.data.append(Question(time,content))
        id = re.findall(r"\"id\":\"(\d+?)\",\"uid", text)

        # check if it is the end
        if (len(id) == 0 or self.all_num > 300000):
            print("all numbers:", self.all_num, len(self.data))
            return
        else:
            self.all_num += len(id)
            next_url = self.live_url_head + id[-1] + self.live_url_last
            yield Request(next_url,meta={'id': current_blogger}, callback=self.parse_live)
            return





    def parse_blogger(self,response):
        data = response.body
        text = data.decode('unicode_escape').replace('\\','')
        # print(text)
        id_tem = re.findall(r"\"uid\":\"(\d+?)\",\"name", text)
        follow_num_tem = re.findall(r"\"follow_num\":(\d+?),", text)
        like_num_tem = re.findall(r"\"like_num\":\"(\d+?)\"", text)
        view_num_tem = re.findall(r"\"view_num\":\"(\d+?)\",\"col", text)

        if(len(id_tem) > 0):
            self.id += id_tem
            self.follow_num += follow_num_tem
            self.like_num += like_num_tem
            self.view_num += view_num_tem
            # next page
            self.url_num += 1
            next_url = self.url_head + str(self.url_num) + self.url_last
            for current_blogger in id_tem:
                if(current_blogger == " "):
                    print(id_tem)
                    time.sleep(20);
                live_url= "http://app.finance.sina.com.cn/course/index.php?callback=jsonp_&s=program&a=ask_detail&format=json&uid="+ current_blogger +"&askuid=&pagesize=100&isans=0&per=" + self.live_url_last
                yield Request(live_url, meta={'id': current_blogger}, callback=self.parse_live)
            yield Request(next_url, callback=self.parse_blogger)
        else:
            print(len(self.id), self.url_num)
            print(self.id)
            return

    # get all content in the homepage
    def parse_homepage(self, response):
        data = response.body
        text = data.decode('unicode_escape').replace('\\', '')
        time = re.findall(r"\"time\":(\d+?),\"", text)
        if (len(time) == 0 or self.all_num > 50000):
            print("all numbers:", self.all_num)
            return
        else:
            self.all_num += len(time)
            next_url = self.url_head + str(int(time[-1]) - 1) + self.url_last
            print(self.time_translate(time[-1]))
            yield Request(next_url, callback=self.parse_homepage)
            return

        # extract contents
        blocks = re.findall(r"{\"(.+?)islive", text)
        for block in blocks:
            content = re.findall(r"content\":\"(.+?)\",\"", block)
            if (content):
                print("content", content[0])
            else:
                question = re.findall(r"question\":\"(.+?)\",\"answer", block)
                answer = re.findall(r"answer\":\"(.+?)\",\"", block)
                print(question[0], answer[0])



        # money_list = response.xpath("//div[@class='f-list-item ershoufang-list']/dl/dd[5]/div[1]/span[1]/text()").extract();
        # title_list = response.xpath("//div[@class='f-list-item ershoufang-list']/dl/dd[1]/a/text()").extract();

    def time_translate(self,timestamp):
        timestamp = int(timestamp)
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt;