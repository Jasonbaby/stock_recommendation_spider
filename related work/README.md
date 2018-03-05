# 阅读相关论文的笔记


## Influence of Social Media over the Stock Market
这篇文章主要分析了投资者在社交媒体上的表现、以及社交媒体对于市场的影响; 研究对象为芝加哥期权交易所市场波动指数VIX(Chicago Board Options Exchange Market Volatility Index)、StockTwits.com网站上用户的表现。

### 流程、模型
先将个体分为两类人：技术型投资者(使用技术分析做投资依据)、非技术型投资者(使用宏观经济等做为投资依据)

使用Stanford CoreNLP Natural Language Processing Toolkit对文本进行情感分类。

#### *Logit models*
Logit模型关注个体的不同因素对因变量(VIX的方差)的影响。 考虑的因素有：投资经历长短、情绪、持仓时间、关注数量、Monthly dummy variables

结果发现只有temporal dummies这个因素对于技术型投资者的影响比较明显。对于非技术型投资者，信息所透露出的情感，影响更显著。

#### *fsQCA(fuzzy-set qualitative comparative analysis)*
fsQCA分析了影响因子组合产生的效应。

结果表明。虽然不同因子之间的组合确实存在着对市场有影响的关系，但是这种影响还是需要视投资者的类型而定。对于技术型投资者而言，经历长短、持仓周期考虑更多。对于非技术型投资者而言，经历长短和情感影响更大。


### 结论

- *社交媒体上的情绪对市场有影响*

- *投资者的个人特征对于解释上述的影响有很关键的作用*


---

## Giving Content to Investor Sentiment: The Role of Media in the Stock Market
这篇文章通过研究华尔街日报专栏中的每日内容，来衡量媒体和股市之间的关系。


### 流程、模型

#### *GI 和 主成分分析*
作者使用General Inquirer (GI)收集数据。 然后对GI预定义的类别中的单词进行主成分因子分析；这样可将77个类别分解成单个媒体因素，以捕捉GI类别中的最大差异。
然后再用得到的因素来衡量悲观程度。

#### *基本向量自回归（VAR）*
衡量悲观因素的变化和股市变化之间的关系，从而来估计媒体悲观主义和股市之间的跨期联系。。



### 结论
作者发现，媒体的高悲观情况往往预测着市场价格下行但随后回归基本面；异常高或低的悲观情况预测高市场交易量；市场的低回报率会导致媒体的悲观情绪。 传统的关于媒体信息不会影响资产价格的学说在这个研究成果面前是不成立的

---


## The Effects of Twitter Sentiment on Stock Price Returns
这篇文章主要研究Twitter和金融市场之间的关系。研究的是跟组成道琼斯指数的30家公司有关的博文。

### 流程、模型

#### *情感分类*

#### *event study*

### 结论

发现整个时间段内相应时间序列之间的Pearson相关性和Granger因果关系相对较低。

在推特量的峰值期间发现Twitter情绪与异常回报之间的显着依赖性。