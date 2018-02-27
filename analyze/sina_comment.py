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
    #删除网址分词
    jieba.suggest_freq('https',tune=False)
    jieba.suggest_freq('com',tune=False)

# 统计词频
def wordcount(str):
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

prepare()
data = pd.read_csv('SINA_data.csv',encoding='gbk')
# 分析提问文本中的词频
question = data['question'].dropna(how = 'any').values
question_text = ""
for q in question:
    question_text += q
question_analyze = jieba.analyse.extract_tags(question_text, topK=50, withWeight=False, allowPOS=())
question_analyze_split = " ".join(question_analyze)
question_lists = question_analyze_split.split(' ')
print(question_lists)

# 分析回答文本中的词频
answer = data['answer'].dropna(how = 'any').values
answer_text = ""
for a in answer:
    answer_text += a
answer_analyze = jieba.analyse.extract_tags(answer_text, topK=50, withWeight=False, allowPOS=())
answer_analyze_split = " ".join(answer_analyze)
answer_lists = answer_analyze_split.split(' ')
print(answer_lists)

# seg_list = jieba.cut(answer_text, cut_all=False) 
# words_split = " ".join(seg_list)
# wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
# my_wordcloud = wc.generate(words_split)
# plt.imshow(my_wordcloud)
# plt.axis("off")
# plt.show()