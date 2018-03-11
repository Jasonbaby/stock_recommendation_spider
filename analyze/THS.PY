import tushare as ts
import pandas as pd
import numpy as np
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

remove_word = ['10', '12', '11', '50', '20']

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

def generate_wordcloud(data):
    #制作词云
    title_list = data['title'].dropna(how = 'any').values
    article_list = data['text'].dropna(how = 'any').values
    title_text = ""
    article_text = ""
    for t in title_list:
        title_text += t
    for a in article_list:
        article_text += a 

    title_words = " ".join(jieba.cut(title_text, cut_all=False) )
    title_wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
    title_wordcloud = title_wc.generate(title_words)
    plt.imshow(title_wordcloud)
    plt.axis("off")
    plt.title('WordCloud of title text')
    plt.show()

    article_words = " ".join(jieba.cut(article_text, cut_all=False) )
    article_wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
    article_wordcloud = article_wc.generate(article_words)
    plt.imshow(article_wordcloud)
    plt.axis("off")
    plt.title('WordCloud of article text')
    plt.show()

prepare()
blogger = pd.read_csv('THS_BLOGGER.csv',encoding='gbk').dropna(how = 'any')
blogger['title abstract'] = None
blogger['article number'] = 0
blogger['article abstract'] = None
data = pd.read_csv('THS_data.csv',encoding='gbk')

title_list = data['title'].dropna(how = 'any').values
text_list = data['text'].dropna(how = 'any').values
title_text = ''
text_text = ''
for t in title_list:
    title_text += t
for t in text_list:
    text_text += t

#title_word_list, title_all_num = wordcount(title_text)
text_word_list, text_all_num =  wordcount(text_text)

#print(title_word_list[0:100], title_all_num)
print(text_word_list[0:100])
exit()

title_words = " ".join(jieba.analyse.extract_tags(title_text, topK=50, withWeight=False, allowPOS=())).split(' ')
print(title_words)
text_words = " ".join(jieba.analyse.extract_tags(text_text, topK=50, withWeight=False, allowPOS=())).split(' ')
print(text_words)
exit()
id_list = list(set(data['id'].values))
print('generating frequent words...')
for ids in id_list:
    TemData = data[data.id == ids]
    # 标题
    title = TemData['title'].dropna(how = 'any').values
    title_result_list, title_count_list, title_word_all_num = analyze(title)
    # 文章内容
    text = TemData['text'].dropna(how = 'any').values
    text_result_list, text_count_list, text_word_all_num = analyze(text)
    pos = blogger[blogger.id == ids].index
    blogger.at[pos,'title abstract'] = ','.join(title_result_list)
    blogger.at[pos,'article abstract'] = ','.join(text_result_list)
    blogger.at[pos,'article number'] = len(text)

blogger.to_csv('detailed_THS_blogger.csv', encoding="utf_8_sig")
print('generating WordCloud...')
# generate_wordcloud(data)

