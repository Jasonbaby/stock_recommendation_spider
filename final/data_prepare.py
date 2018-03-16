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




title_frequent = ['当天出现的文章','市场', '公司', '投资', '中国', '三板', '股市', '2017', \
'什么', '机会', '如何', '大盘', '涨停', '行情', '反弹', \
'大盘', '反弹', '涨停', '如何', '行情', '投资', '板块', \
'板块', '金融', '上市', '分析', '企业', '概念', '12', \
'资金', '关注', '个股', '银行', 'IPO', '创业板', '2018', \
'交易', '龙头', '基金', '今日', '科技', '这些', '操作', \
'调整', '复盘', '股民', '11', '热点', '数据', '业绩', '主力','概念股','利好','风险','策略',\
'有望','震荡','技术','未来','爆发','新高','持续','上涨','跌停','趋势','增长','注意','重磅',\
'抄底','买入']

text_frequent = ['当天出现的文章','公司','市场', '投资', '中国', '企业',  '我们', '资金', '可以','亿元', '行业',  '没有', '交易', '金融','银行', '股份',  '发展','股票', '这个', '增长',\
'板块','产品', '可能','指数', '数据', '出现', '技术', '上市', '目前','业务', '如果','个股''今天','科技', '经济', '风险', '还是', '价格', '上涨', '投资者', \
'时间', '基金', '主要', '资产','股价', '开始','创业','问题','方面','因为', '服务','自己','但是', '业绩','股东','不是','机构', '现在', '管理', '产业', '通过', '利润', \
'对于', '证券', '继续', '未来', '平台', '进行', '分析', '第一', '需要', '情况', '万元', '反弹', '行情', '成为', '12', '下跌', '美元', '持续', '调整', '集团', '影响', \
'股市', '消费', '收入','创业板','美国','趋势']


data = pd.read_csv('THS_data.csv',encoding='gbk')
# data.pop('text')
time_all = data['time']
title_list = data['text']
time_l = []


for i in range(0, len(time_all)):
    time_l.append(time_all[i].split(' ')[0]) #.replace('-','/'))



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
time_list_sh = sh['date'].tolist()
time_list_sz = sz['date'].tolist()
time_list_hs300 = hs300['date'].tolist()
time_list_sz50 = sz50['date'].tolist()
time_list_zxb = zxb['date'].tolist()
time_list_cyb = cyb['date'].tolist()


other_attr = ['后五日涨跌幅','后十日涨跌幅','前五日涨跌幅','前十日涨跌幅'] # 14
for key_word in other_attr:
    sh[key_word] = None
    sz[key_word] = None
    hs300[key_word] = None
    sz50[key_word] = None
    zxb[key_word] = None
    cyb[key_word] = None

for i in range(0, len(sh)):
    if(i >= 5):
        shp = (sh.iloc[i,3] - sh.iloc[i-5,3]) / sh.iloc[i,3]
        sh.iat[i,14] = shp
        sh.iat[i-5,16] = shp
        szp = (sz.iloc[i,3] - sz.iloc[i-5,3]) / sz.iloc[i,3]
        sz.iat[i,14] = szp
        sz.iat[i-5,16] = szp
        hs300p = (hs300.iloc[i,3] - hs300.iloc[i-5,3]) / hs300.iloc[i,3]
        hs300.iat[i,14] = hs300p
        hs300.iat[i-5,16] = hs300p
        sz50p = (sz50.iloc[i,3] - sz50.iloc[i-5,3]) / sz50.iloc[i,3]
        sz50.iat[i,14] = sz50p
        sz50.iat[i-5,16] = sz50p
        zxbp = (zxb.iloc[i,3] - zxb.iloc[i-5,3]) / zxb.iloc[i,3]
        zxb.iat[i,14] = zxbp
        zxb.iat[i-5,16] = zxbp
        cybp = (cyb.iloc[i,3] - cyb.iloc[i-5,3]) / cyb.iloc[i,3]
        cyb.iat[i,14] = cybp
        cyb.iat[i-5,16] = cybp
    if(i >= 10):
        shp = (sh.iloc[i,3] - sh.iloc[i-10,3]) / sh.iloc[i,3]
        sh.iat[i,15] = shp
        sh.iat[i-10,17] = shp
        szp = (sz.iloc[i,3] - sz.iloc[i-10,3]) / sz.iloc[i,3]
        sz.iat[i,15] = szp
        sz.iat[i-10,17] = szp
        hs300p = (hs300.iloc[i,3] - hs300.iloc[i-10,3]) / hs300.iloc[i,3]
        hs300.iat[i,15] = hs300p
        hs300.iat[i-10,17] = hs300p
        sz50p = (sz50.iloc[i,3] - sz50.iloc[i-10,3]) / sz50.iloc[i,3]
        sz50.iat[i,15] = sz50p
        sz50.iat[i-10,17] = sz50p
        zxbp = (zxb.iloc[i,3] - zxb.iloc[i-10,3]) / zxb.iloc[i,3]
        zxb.iat[i,15] = zxbp
        zxb.iat[i-10,17] = zxbp
        cybp = (cyb.iloc[i,3] - cyb.iloc[i-10,3]) / cyb.iloc[i,3]
        cyb.iat[i,15] = cybp
        cyb.iat[i-10,17] = cybp



for key_word in text_frequent:
    sh[key_word] = 0
    sz[key_word] = 0
    hs300[key_word] = 0
    sz50[key_word] = 0
    zxb[key_word] = 0
    cyb[key_word] = 0





frequent_count = 0
for i in range(0, len(title_list)):
    title = title_list[i]
    time_stamp_sh = find_pos(time_list_sh, time_l[i])
    time_stamp_sz = find_pos(time_list_sz, time_l[i])
    time_stamp_hs300 = find_pos(time_list_hs300, time_l[i])
    time_stamp_sz50 = find_pos(time_list_sz50, time_l[i])
    time_stamp_zxb = find_pos(time_list_zxb, time_l[i])
    time_stamp_cyb = find_pos(time_list_cyb, time_l[i])

    sh.at[time_stamp_sh, '当天出现的文章'] += 1
    hs300.at[time_stamp_hs300, '当天出现的文章'] += 1
    sz50.at[time_stamp_sz50, '当天出现的文章'] += 1
    zxb.at[time_stamp_zxb, '当天出现的文章'] += 1
    cyb.at[time_stamp_cyb, '当天出现的文章'] += 1
    sz.at[time_stamp_sz, '当天出现的文章'] += 1

    word_list = jieba.lcut(title, cut_all=True) 
    for word in word_list:
        if(len(word) < 2):
            continue
        elif(word in text_frequent):
            frequent_count += 1
            sh.at[time_stamp_sh, word] += 1
            hs300.at[time_stamp_hs300, word] += 1
            sz50.at[time_stamp_sz50, word] += 1
            zxb.at[time_stamp_zxb, word] += 1
            cyb.at[time_stamp_cyb, word] += 1
            sz.at[time_stamp_sz, word] += 1
    


print(frequent_count)

sh.to_csv('result/sh_text_analyze.csv')
sz.to_csv('result/sz_text_analyze.csv')
hs300.to_csv('result/hs300_text_analyze.csv')
sz50.to_csv('result/sz50_text_analyze.csv')
zxb.to_csv('result/zxb_text_analyze.csv')
cyb.to_csv('result/cyb_text_analyze.csv')