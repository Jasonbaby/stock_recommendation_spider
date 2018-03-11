import pandas as pd
import tushare as ts
import numpy as np
import jieba
import jieba.analyse


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



# ts.get_hist_data('sh').to_csv('sh.csv') #获取上证指数k线数据
# ts.get_hist_data('sz').to_csv('sz.csv') #获取深圳成指k线数据
# ts.get_hist_data('hs300').to_csv('hs300.csv') #获取沪深300指数k线数据
# ts.get_hist_data('sz50').to_csv('sz50.csv') #获取上证50指数k线数据
# ts.get_hist_data('zxb').to_csv('zxb.csv') #获取中小板指数k线数据
# ts.get_hist_data('cyb').to_csv('cyb.csv') #获取创业板指数k线数据

sh = pd.read_csv('sh.csv',encoding='gbk') #获取上证指数k线数据
sz = pd.read_csv('sz.csv',encoding='gbk') #获取深圳成指k线数据
hs300 = pd.read_csv('hs300.csv',encoding='gbk') #获取沪深300指数k线数据
sz50 = pd.read_csv('sz50.csv',encoding='gbk') #获取上证50指数k线数据
zxb = pd.read_csv('zxb.csv',encoding='gbk') #获取中小板指数k线数据
cyb = pd.read_csv('cyb.csv',encoding='gbk') #获取创业板指数k线数据

sh.index = sh['date'].tolist()
sz.index = sz['date'].tolist()
hs300.index = hs300['date'].tolist()
sz50.index = sz50['date'].tolist()
zxb.index = zxb['date'].tolist()
cyb.index = cyb['date'].tolist()

# 交易日
time_list = sh['date'].tolist()

for key_word in title_frequent:
    sh[key_word] = 0
    sz[key_word] = 0
    hs300[key_word] = 0
    sz50[key_word] = 0
    zxb[key_word] = 0
    cyb[key_word] = 0

for i in range(0, len(title_list)):
    title = title_list[i]
    time_stamp = find_pos(time_list, time_l[i])
    word_list = jieba.lcut(title, cut_all=True) 
    for word in word_list:
        if(len(word) < 2):
            continue
        elif(word in title_frequent):
            sh.at[time_stamp, word] += 1
            sz.at[time_stamp, word] += 1
            hs300.at[time_stamp, word] += 1
            sz50.at[time_stamp, word] += 1
            zxb.at[time_stamp, word] += 1
            cyb.at[time_stamp, word] += 1

sh.to_csv('result/sh_analyze.csv')
sz.to_csv('result/sz_analyze.csv')
hs300.to_csv('result/hs300_analyze.csv')
sz50.to_csv('result/sz50_analyze.csv')
zxb.to_csv('result/zxb_analyze.csv')
cyb.to_csv('result/cyb_analyze.csv')