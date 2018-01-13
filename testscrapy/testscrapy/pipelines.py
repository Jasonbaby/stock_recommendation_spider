# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import csv
import time
class TestscrapyPipeline(object):
    def open_spider(self,spider):
        self.all_num = 0
        self.out = open('D:\live_data.csv', 'w', newline='')
        self.csv_write = csv.writer(self.out, dialect='excel')
        return


    def process_item(self, item, spider):
        self.csv_write.writerows([[item['id'], item['q_timestamp'], item['question'], item['a_timestamp'], item['answer'] ]])
        self.all_num += 1
        return item


    def spider_close(self, spider):
        self.out.close()
        print(self.all_num)
