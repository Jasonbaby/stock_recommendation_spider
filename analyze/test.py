# 对新浪财经博主的个性签名进行词频统计，并制作成词云
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
lists = analyze_split.split(' ')
print(lists)

wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
my_wordcloud = wc.generate(words_split)
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

