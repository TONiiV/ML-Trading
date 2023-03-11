
# # 定义Yahoo财经的下载链接和请求参数
# code = '^TNX'
# url = f"https://query1.finance.yahoo.com/v7/finance/download/{code}"
# params = {
#     "period1": "1420066800", # 开始时间，以Unix时间戳表示 2015.01.01
#     "period2": "1677625200", # 结束时间，以Unix时间戳表示 2023.03.01
#     "interval": "1d", # 时间间隔，可以是1d（每日）、1wk（每周）、1mo（每月）
#     "events": "history", # 事件类型，可以是history（历史数据）、div（分红）、split（拆股）
#     "includeAdjustedClose": "true" # 是否包含调整后的收盘价
# }

import requests
from lxml import html
import pandas as pd
import json as json
import os
import yfinance as yf

def get_data(
        data_type,
        data_name,
        start_time,
        end_time,
        interval = "1d",
        events = "history",
        save_data = False
    ):
    cwd = os.path.join(os.path.dirname(__file__),'..')
    codes = os.path.join(cwd, 'codes.json')
    with open(codes, 'r') as f:
        codes = json.load(f)
    code = codes[data_type][data_name]

    # url = f"https://query1.finance.yahoo.com/v7/finance/download/{code}"
    # headers = {"User-Agent": "Mozilla/5.0"}
    # params = {
    #     "period1": start_time, # 开始时间，以Unix时间戳表示
    #     "period2": end_time, # 结束时间，以Unix时间戳表示
    #     "interval": interval, # 时间间隔，可以是1d（每日）、1wk（每周）、1mo（每月）
    #     "events": events, # 事件类型，可以是history（历史数据）、div（分红）、split（拆股）
    #     "includeAdjustedClose": "true" # 是否包含调整后的收盘价
    # }
    # response = requests.get(url, headers=headers, params=params)
    # content = response.content
    # csv = str(content)[2:-1]
    # # 2. convert string to csv
    # csv = csv.replace('\\t', ',').replace('\\n', '\n')
    # if save_data:
    #     save_path = os.path.join(cwd, 'Data', data_type, f'{data_name}.csv')
    #     print(csv, file=open(save_path, 'w'))

    data = yf.download(code, start=start_time, end=end_time, interval = interval)
    print(data, type(data))

    if save_data:
        save_path = os.path.join(cwd, 'Data', data_type, f'{start_time}-to-{end_time}-{interval}')
        if not os.path.exists(save_path):
            print(1)
            os.mkdir(save_path)
        file_path = os.path.join(save_path, f'{data_name}.csv')
        data.to_csv(file_path,sep=',')


if __name__ == '__main__' :
    cwd = os.path.join(os.path.dirname(__file__),'..')
    codes = os.path.join(cwd, 'codes.json')
    with open(codes, 'r') as f:
        codes = json.load(f)

    dtype = 'Commodity'
    for name in codes[dtype].keys():
        get_data(
            dtype, 
            name, 
            "2022-01-01", 
            "2023-03-01", 
            interval='1h', 
            save_data=True
        )