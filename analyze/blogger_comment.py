import tushare as ts
import pandas as pd
import numpy as np
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 得到所有股票的代码和中文名字，将其作为新词录入词典
def prepare():
    df = ts.get_stock_basics()
    name = df['name']
    code = name.index.tolist()
    namelist = name.values.tolist()
    for c in code:
        jieba.add_word(c)
    for n in namelist:
        jieba.add_word(n)

# 统计词频,由于jieba库没有统计词频的功能，因此这块要额外写
def wordcount(text):
    # 文章字符串前期处理
    strl_ist = jieba.lcut(text, cut_all=True) 
    count_dict = {}
    all_num = 0;
    # 如果字典里有该单词则加1，否则添加入字典
    for str in strl_ist:
        if(len(str) <= 1):
            continue
        else:
            all_num+=1
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    #按照词频从高到低排列
    count_list=sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
    return count_list, all_num


# 将得到的文本的list，进行分析
def analyze(text_list):
    text = ""
    for t in text_list:
        text += t
    analyze = jieba.analyse.extract_tags(text, topK=50, withWeight=False, allowPOS=())
    result_list = " ".join(analyze).split(' ')
    count_list, all_num = wordcount(text)
    return result_list, count_list, all_num

prepare()
blogger = pd.read_csv('SINA_BLOGGER.csv',encoding='gbk').dropna(how = 'any')
blogger['question abstract'] = None
blogger['question number'] = 0
blogger['answer abstract'] = None
blogger['answer number'] = 0
data = pd.read_csv('SINA_data.csv',encoding='gbk')
id_list = list(set(data['id'].values))
for ids in id_list:
    TemData = data[data.id == ids]
    # 提问的文本
    question = TemData['question'].dropna(how = 'any').values
    q_result_list, q_count_list, q_all_num = analyze(question)
    # 回答的文本
    answer = TemData['answer'].dropna(how = 'any').values
    a_result_list, a_count_list, a_all_num = analyze(answer)
    pos = blogger[blogger.id == ids].index
    blogger.at[pos,'question abstract'] = ','.join(q_result_list)
    blogger.at[pos,'question number'] = len(question)
    blogger.at[pos,'answer abstract'] = ','.join(a_result_list)
    blogger.at[pos,'answer number'] = len(answer)
blogger.to_csv('detailed_blogger.csv', encoding="utf_8_sig")

