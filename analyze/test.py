import tushare as ts
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud


def wordcount(str):
    # 文章字符串前期处理
    seg_list = jieba.cut(text, cut_all=False) 
    words_split = " ".join(seg_list)
    strl_ist = words_split.split(' ')
    count_dict = {}
    # 如果字典里有该单词则加1，否则添加入字典
    for str in strl_ist:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    #按照词频从高到低排列
    count_list=sorted(count_dict.items(),key=lambda x:x[1],reverse=True)
    return count_list


data = pd.read_csv('SINA_BLOGGER.csv',encoding='gbk')
signature = data.ix[:,'signature']
signature = signature.dropna(how = 'any')
signature = signature.values.tolist()
text = "";
for t in signature :
    text = text + t;
seg_list = jieba.cut(text, cut_all=False) 
words_split = " ".join(seg_list)
analyze = jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=())
analyze_split = " ".join(analyze)
lists = analyze_split.split(' ');
print(wordcount(text))
print(lists)

# wc = WordCloud(font_path="simhei.ttf")    # 字体这里有个坑，一定要设这个参数。否则会显示一堆小方框wc.font_path="simhei.ttf"   # 黑体
# my_wordcloud = wc.generate(words_split)
# plt.imshow(my_wordcloud)
# plt.axis("off")
# plt.show()

