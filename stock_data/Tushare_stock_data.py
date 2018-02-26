import tushare as ts
import pandas as pd
import numpy as np
import os
import sys

# 得到所有股票代码
def get_all_stocks_index():
    df = ts.get_stock_basics()
    all_stock = df.index.tolist()   
    return all_stock

def get_data(code = '000001', min = "5min", start = '20150101', end = '20200101'): #min = "5min"
    df = ts.bar(code, conn=ts.get_apis(), freq=min, start_date = start, end_date = end)
    return df

if __name__ == "__main__":
    all_stock_list = get_all_stocks_index()
    data_save_path = "data/"
    for stock in all_stock_list[0:5]:
        print('reading data from ' + stock)
        df = get_data(code = stock)
        save_path = os.path.join(data_save_path, stock + '.csv')
        df.to_csv(save_path, encoding="utf_8_sig")
    os._exit(0)

