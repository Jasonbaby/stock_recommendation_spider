import time,urllib
import urllib.request
import http.client
import re
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
# 获取页面数据
def get_page(url):  
    req=urllib.request.Request(url,headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    opener=urllib.request.urlopen(req)
    page=opener.read()
    return page


# 获取股票代码列表
def urlTolist(url):
    allCodeList = []
    # 获取原始数据
    try:
        html = get_page(url).decode('gb2312') 
    except http.client.IncompleteRead as e:  # 异常处理，这里可能会导致数据不全
        html = e.partial.decode('gb2312') 
    
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0]=='6' or item[0]=='3' or item[0]=='0': # select the code of stocks
            allCodeList.append(item)
    return allCodeList


def get_index_history_byNetease(index_temp):
    """
    :param index_temp: for example, 'sh000001' 上证指数
    :return:
    """
    index_type=index_temp[0:2]
    index_id=index_temp[2:]
    if index_type=='sh':
        index_id='0'+index_id
    if index_type=="sz":
        index_id='1'+index_id
    url='http://quotes.money.163.com/service/chddata.html?code=%s&start=19900101&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'%(index_id,time.strftime("%Y%m%d"))

    page=get_page(url).decode('gb2312') #该段获取原始数据
    page=page.split('\r\n')
    col_info=page[0].split(',')   #各列的含义
    index_data=page[1:]     #真正的数据

    #为了与现有的数据库对应，这里我还修改了列名，大家不改也没关系
    col_info[col_info.index('日期')]='交易日期'   #该段更改列名称
    col_info[col_info.index('股票代码')]='指数代码'
    col_info[col_info.index('名称')]='指数名称'
    col_info[col_info.index('成交金额')]='成交额'

    index_data=[x.replace("'",'') for x in index_data]  #去掉指数编号前的“'”
    index_data=[x.split(',') for x in index_data]

    index_data=index_data[0:index_data.__len__()-1]   #最后一行为空，需要去掉
    pos1=col_info.index('涨跌幅')
    pos2=col_info.index('涨跌额')
    posclose=col_info.index('收盘价')
    index_data[index_data.__len__()-1][pos1]=0      #最下面行涨跌额和涨跌幅为None改为0
    index_data[index_data.__len__()-1][pos2]=0
    for i in range(0,index_data.__len__()-1):       #这两列中有些值莫名其妙为None 现在补全
        if index_data[i][pos2]=='None':
            index_data[i][pos2]=float(index_data[i][posclose])-float(index_data[i+1][posclose])
        if index_data[i][pos1]=='None':
            index_data[i][pos1]=(float(index_data[i][posclose])-float(index_data[i+1][posclose]))/float(index_data[i+1][posclose])

    # print(col_info)
    return [index_data,col_info]

if __name__ == '__main__':
    print (get_index_history_byNetease('sh000001'))
    # stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html';   
    # print(urlTolist(stock_CodeUrl))
