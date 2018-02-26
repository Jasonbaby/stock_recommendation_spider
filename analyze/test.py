
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud

data = pd.read_csv('SINA_BLOGGER.csv',encoding='gbk')
signature = data.ix[:,'signature']
signature = signature.dropna(how = 'any')
signature = signature.values.tolist()
text = "";
for t in signature :
    text = text + t;
seg_list = jieba.cut(text, cut_all=False) 
words_split = " ".join(seg_list)

wc = WordCloud(font_path="simhei.ttf")    # 字体这里有个坑，一定要设这个参数。否则会显示一堆小方框wc.font_path="simhei.ttf"   # 黑体
my_wordcloud = wc.generate(words_split)
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
# import jieba

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# seg_list = jieba.cut("我来到北京清华大学", cut_all=False) 
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))

# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

# str = "我来到北京清华大学,今天好开心哦，今天天气真好";
# tags = jieba.analyse.extract_tags(str, topK=5)
# print("关键词:    ", " / ".join(tags))