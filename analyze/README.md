## 词频统计、分析
使用库：

[结巴分词系统](https://github.com/fxsjy/jieba)、wordcloud
### 算法
- 基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
- 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
- 对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法

### 流程
#### sina_blogger.py 
对新浪财经的博主的个性签名进行词频统计并制作成词云

![image](https://note.youdao.com/yws/public/resource/0882535f1a2cd291ea2a63d5fc68e619/WEBRESOURCE9f58c71f3bb94c4dfda97735351a1d0b)

#### sina_comment.py 
对所有主播直播间的提问和回答进行词频统计并制作成词云

![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCEb031d3748cf534eb284bb7a5161b0ce2/2277)
![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCEcaef8ea18a0f3646cfa30ba2c6db2e9b/2275)

#### blogger_comment.py
分别对所有主播的提问和回答进行词频统计，并将得到的高频词保存下来，丰富主播的信息