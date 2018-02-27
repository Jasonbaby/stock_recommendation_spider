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
    jieba.del_word('https')
    jieba.del_word('com')
prepare()
data = pd.read_csv('SINA_data.csv',encoding='gbk')
question = data['question']
question = question.dropna(how = 'any')
question = question.values
question_text = ""
for q in question:
    question_text += q
analyze = jieba.analyse.extract_tags(question_text, topK=20, withWeight=False, allowPOS=())
analyze_split = " ".join(analyze)
lists = analyze_split.split(' ')
print(lists)

answer = data['answer']
answer = answer.dropna(how = 'any')
answer = answer.values
answer_text = ""
for a in answer:
    answer_text += a
answer_analyze = jieba.analyse.extract_tags(answer_text, topK=20, withWeight=False, allowPOS=())
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