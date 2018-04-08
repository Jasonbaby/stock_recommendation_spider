import pandas as pd
import numpy as np

word_col = ['当天出现的文章','市场', '公司', '投资', '中国', '三板', '股市', '2017', \
'什么', '机会', '如何', '大盘', '涨停', '行情', '反弹', \
'大盘', '涨停', '如何', '行情', '投资', '板块', \
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

market_col = ['后五日涨跌幅','后十日涨跌幅','前五日涨跌幅','前十日涨跌幅','volume','p_change']


file_list = ['cyb_text_analyze.csv','hs300_text_analyze.csv','sh_text_analyze.csv','sz_text_analyze.csv','sz50_text_analyze.csv','zxb_text_analyze.csv']

for file in file_list:
    market = file.split('_')[0]
    # fin = open('corr/' + file)
    data = pd.read_csv('result/'+file,encoding='gbk')
    data = data[data.当天出现的文章 > 100]

    select_data = data.loc[:,word_col + market_col]

    for market_data in market_col:
        for word in text_frequent:
            select_data = data.loc[:,[market_data,word]]
            cor = select_data.corr().iloc[0,1]
            if(abs(cor) > 0.2):
                print(market,'|',word,'|',market_data,'|',cor)
