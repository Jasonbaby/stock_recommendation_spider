# 使用爬虫获取财经网站的评论、文章
## 环境
python 3.6 + scrapy 1.5.0 + pycharm 2017.3.2

这是本人第一个正规的爬虫项目，细节处难免疏漏，若发现有错误或者不清楚的地方，请及时与我联系。 jiexin_zheng@qq.com

## 爬取数据
新浪财经直播网，所有主播的全部问答。 网站内容可见: http://live.finance.sina.com.cn/bozhu/1216826604
同花顺同顺号，所有主播的文章。网站内容可见：http://master.10jqka.com.cn/master_list.shtml

### 新浪数据: 
1. 博主的id，名称，关注的数量，获赞数量，访问数量

![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCEf6a3cd49456425b72861c0c598da487d/2231)

2. 博主的id，提问时间，提问内容，回答时间，回答内容

![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCE83669c2588988c427898f1fb5ae65770/2233)


### 同花顺数据：

1. 博主的id，名称，关注的数量，文章的数量，访问数量

![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCE4cbc306736b335599ca179cb6654be6c/2235)


2. 博主的id，时间，文章内容

![image](https://note.youdao.com/yws/public/resource/5b1e49db8425a9748610af71880bbcbc/xmlnote/WEBRESOURCE2e875913b4f29c1e6030569d7745ad9c/2237)

## 运行

进入到项目目录后
```
scrapy crawl sina  #爬取新浪财经的数据
scrapy crawl ths   #爬取同花顺的数据
```

## 运行结果
在新浪财经上，爬取到283位主播的信息，得到257972条问答数据

在同花顺上，爬取到1310位博主的信息，得到72462篇文章数据

