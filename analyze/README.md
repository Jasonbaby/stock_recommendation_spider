## 词频统计、分析
使用库：

[结巴分词系统](https://github.com/fxsjy/jieba)、wordcloud
### 算法
- 基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
- 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
- 对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法

### 效果
![image](https://note.youdao.com/yws/res/2258/WEBRESOURCE9f58c71f3bb94c4dfda97735351a1d0b)