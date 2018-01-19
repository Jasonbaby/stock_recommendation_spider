# 股票数据获取方法

## 使用Tushare库获取数据
https://github.com/waditu/tushare

TuShare是实现对股票/期货等金融数据从数据采集、清洗加工 到 数据存储过程的工具，满足金融量化分析师和学习数据分析的人在数据获取方面的需求，它的特点是数据覆盖范围广，接口调用简单,响应快速。

Tushare_stock_data.py 是使用的demo，运行之后可以获得所有股票的日线历史数据，并保存为csv文件

## 通过网易接口获取历史数据

用起来不方便，不建议用，Netease_stock_data.py文件里的是使用的demo