# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
class TestscrapyPipeline(object):
    def open_spider(self,spider):
        if(spider.name == 'sina'):
            self.all_num = 0
            self.out = open('D:\SINA_data.csv', 'w', newline='')
            self.csv_write = csv.writer(self.out, dialect='excel')
            self.csv_write.writerows([['id','question time','question','answer time','answer']])
            return


    def process_item(self, item, spider):
        if (spider.name != "sina"):
            return item
        self.csv_write.writerows([[item['id'], item['q_timestamp'], item['question'], item['a_timestamp'], item['answer'] ]])
        self.all_num += 1


    def spider_close(self, spider):
        if (spider.name == 'sina'):
            self.out.close()
            print(self.all_num)


class THSPipeline(object):
    def open_spider(self,spider):
        if (spider.name == 'ths'):
            self.all_num = 0
            self.out = open('D:\THS_data.csv', 'w', newline='')
            self.csv_write = csv.writer(self.out, dialect='excel')
            self.csv_write.writerows([['id','time','title','text']])


    def process_item(self, item, spider):
        if (spider.name == "ths" ):
            self.csv_write.writerows([[item['id'], item['time'], item['title'], item['text']]])
            self.all_num += 1
            if(self.all_num % 100 == 0):
                print('The recent number:',self.all_num)


    def spider_close(self, spider):
        if (spider.name == 'ths'):
            self.out.close()
            print(self.all_num)