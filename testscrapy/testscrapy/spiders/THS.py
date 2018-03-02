import scrapy
import re
import time
import csv
from ..items import  THS_BLOG,THS_BLOGGER
from ..struct import Content,Question
from scrapy.http import Request
class THSSpider(scrapy.Spider):
    name = "ths"
    parse_mode = "blogger"
    start_urls = ["http://master.10jqka.com.cn/master_list.shtml"]


    def parse(self, response):
        self.all_num = 0
        self.current_blogger = ''
        self.paper_url_1 = "http://master.10jqka.com.cn/mj_"
        self.paper_url_2 = "/index_"
        self.paper_url_3 = ".shtml"
        self.blogger_data = []
        if (self.parse_mode == "blogger"):
            start_urls = "http://comment.10jqka.com.cn/rapi/main.php?method=master.search&callback=master&count=100&start=&sortby=rtime&track=masterlist&_=1515911699805"
            self.url_head = "http://comment.10jqka.com.cn/rapi/main.php?method=master.search&callback=master&count=50&start="
            self.url_last = "&sortby=rtime&track=masterlist&_=1515911699805"
            self.id = []
            yield Request(start_urls, callback=self.parse_blogger)
            return

    def parse_detail(self,response):
        try:
            current_blogger = response.meta['id']
        except:
            current_blogger = ""
        item = THS_BLOG()
        title = response.xpath("//div[@class='main article']/h2/text()").extract()
        if(len(title) == 0):
            return
        title = response.xpath("//div[@class='main article']/h2/text()").extract()[0]
        time =  response.xpath("//div[@class='time']/span[1]/text()").extract()[0]
        text = response.xpath("//div[@class='article-con']")[0].xpath('string(.)').extract()[0]
        text = text.replace('\xa0','')
        item['id'] = current_blogger
        item['time'] = time
        item['title'] = title
        item['text'] = text
        yield item

    def parse_paper(self,response):
        try:
            current_page = response.meta['count']
            id = response.meta['id']
        except:
            current_page = 0
            id = "0"
        # get the detail of papers
        paper_address = response.xpath("//div[@class='listTit clearfix']/a/@href").extract()
        for address in paper_address:
            yield Request(address, callback=self.parse_detail, meta={'id': id})
        if(len(paper_address) > 0):
            next_url = self.paper_url_1 + str(id) + self.paper_url_2 + str(current_page + 1) + self.paper_url_3
            yield Request(next_url, callback=self.parse_paper, meta={'id': id, 'count': (current_page+1)})


    def parse_blogger(self,response):
        text = response.body.decode('unicode_escape').replace('\\','')
        id = re.findall(r"{\"id\":(\d+?),\"uid", text)
        name = re.findall(r"\"name\":\"(.+?)\",", text)
        like_num = re.findall(r"\"fans\":(.+?),", text)
        newsNum = re.findall(r"\"newsNum\":(.+?),", text)
        visitNum = re.findall(r"\"pv\":(\d+?),\"name\"", text)
        lastTime = re.findall(r"\"latestnewstime\":(\d+?),\"", text)

        # save the blogger data and find his articile
        if(len(id) > 0):
            self.blogger_data += zip(id,name,like_num,newsNum,visitNum)
            self.id += id
            lastNewsTime = str(int(lastTime[-1])-1)
            next_url = self.url_head + lastNewsTime + self.url_last
            yield Request(next_url, callback=self.parse_blogger)
        else:
            # save the information of blogger
            csvfile = open('D:\THS_BLOGGER.csv', 'w', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(['id','name','like num','paper num','visit num'])
            for data in self.blogger_data:
                writer.writerow(data)
            csvfile.close()
            # save the information of paper
            for id in self.id:
                paper_url = self.paper_url_1 + id + self.paper_url_2 + '0' + self.paper_url_3
                print("new blogger:" , id)
                yield Request(paper_url, callback=self.parse_paper, meta={'id': id, 'count': 0})




        # money_list = response.xpath("//div[@class='f-list-item ershoufang-list']/dl/dd[5]/div[1]/span[1]/text()").extract();
        # title_list = response.xpath("//div[@class='f-list-item ershoufang-list']/dl/dd[1]/a/text()").extract();

    def time_translate(self,timestamp):
        timestamp = int(timestamp)
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt