# 对新浪财经博主的直播室的提问和回答进行分词统计，并制作成词云
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

# 统计词频
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

prepare()
data = pd.read_csv('SINA_data.csv',encoding='gbk')

# 分析提问文本中的词频
question = data['question'].dropna(how = 'any').values
question_text = ""
for q in question:
    question_text += q
question_analyze = jieba.analyse.extract_tags(question_text, topK=50, withWeight=False, allowPOS=())
question_lists = " ".join(question_analyze).split(' ')
print(question_lists)

# 分析回答文本中的词频
answer = data['answer'].dropna(how = 'any').values
answer_text = ""
for a in answer:
    answer_text += a
answer_analyze = jieba.analyse.extract_tags(answer_text, topK=50, withWeight=False, allowPOS=())
answer_lists = " ".join(answer_analyze).split(' ')
print(answer_lists)

answer_seg_list = jieba.cut(answer_text, cut_all=False) 
answer_words_split = " ".join(answer_seg_list)
answer_wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
answer_wordcloud = answer_wc.generate(answer_words_split)
plt.imshow(answer_wordcloud)
plt.axis("off")
plt.title('WordCloud of answer text')
plt.show()


question_seg_list = jieba.cut(question_text, cut_all=False) 
question_words_split = " ".join(question_seg_list)
question_wc = WordCloud(font_path="simhei.ttf", max_words = 50, background_color = 'white', width = 800, height = 500)    
question_wordcloud = question_wc.generate(question_words_split)
plt.imshow(question_wordcloud)
plt.axis("off")
plt.title('WordCloud of question text')
plt.show()
