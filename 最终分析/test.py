import pandas as pd
import tushare as ts
import numpy as np
import jieba
import jieba.analyse



title_frequent = ['A股', '2017', '三板', 'IPO', '2018', '10', '附股', \
'收评', '午评', '12', '复盘', '市场', '股市', '机会', \
'大盘', '反弹', '涨停', '如何', '行情', '投资', '板块', \
'11', '中国', '易选股', '50', '公司', '分析', '个股', \
'概念股', '下周', '雄安', '20', '热点', '股票', '重磅', \
'关注', '金融', '盘前', '指数', '利好', '创业板', '企业', \
'行业', '股民', '抄底', '揭秘', '今日', '资金', '操作', '黄斌汉']


data = pd.read_csv('THS_data.csv',encoding='gbk')
data.pop('text')
time_all = data['time']
title_list = data['title']

time_l = []
for i in range(0, len(time_all)):
    time_l.append(time_all[i].split(' ')[0].replace('-','/'))


    

def find_pos(time_list, time):
    if( time in time_list):
        return time
    elif(time > time_list[0]):
        return time_list[0]
    elif(time < time_list[-1]):
        return time_list[-1]
    else:
        for i in range(0, len(time_list)-1):
            if(time < time_list[i] and time > time_list[i+1]):
                return time_list[i+1]



sh = pd.read_csv('sh.csv',encoding='gbk') #获取上证指数k线数据
sh.index = sh['date'].tolist()

time_list = sh['date'].tolist()
#print(find_pos(time_list,'2015-03-14'))

#sh.at['2015-03-16', 'v_ma10'] = 0



for i in range(0, len(title_list)):
    title = title_list[i]
    time_stamp = find_pos(time_list, time_l[i])
    if(i > 100):
        break
    word_list = jieba.lcut(title, cut_all=True) 
    for word in word_list:
        if(len(word) < 2):
            continue
        elif(word in title_frequent):
            print(time_stamp, word)

