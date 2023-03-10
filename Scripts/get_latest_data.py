
# # 定义Yahoo财经的网址和请求头
# url = "https://finance.yahoo.com/quote/TSLA"
# headers = {"User-Agent": "Mozilla/5.0"}

# # 发送请求并获取响应内容
# response = requests.get(url, headers=headers)
# content = response.content

# # 解析响应内容为HTML树结构
# tree = html.fromstring(content)

# # 从HTML树结构中提取苹果公司的最新股价信息
# info = tree.xpath("//div[@id='quote-summary']//td")

# # # 打印苹果公司的最新股价信息
# # for i in range(0, len(info), 2):
# #     key = info[i].text_content()
# #     value = info[i+1].text_content()
# #     print(key + ": " + value)


# # 定义Yahoo财经的下载链接和请求参数
# code = '^TNX'
# url = f"https://query1.finance.yahoo.com/v7/finance/download/{code}"
# params = {
#     "period1": "1420066800", # 开始时间，以Unix时间戳表示
#     "period2": "1677625200", # 结束时间，以Unix时间戳表示
#     "interval": "1d", # 时间间隔，可以是1d（每日）、1wk（每周）、1mo（每月）
#     "events": "history", # 事件类型，可以是history（历史数据）、div（分红）、split（拆股）
#     "includeAdjustedClose": "true" # 是否包含调整后的收盘价
# }

# # 发送请求并获取响应内容
# response = requests.get(url, headers=headers, params=params)
# content = response.content
# csv = str(content)[2:-1]
# # 2. convert string to csv
# csv = csv.replace('\\t', ',').replace('\\n', '\n')
# print(csv, file=open(f'{code}.csv', 'w'))
import requests
from lxml import html
import pandas as pd
import json as json
import os


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
    #print(code)
    
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "period1": start_time, # 开始时间，以Unix时间戳表示
        "period2": end_time, # 结束时间，以Unix时间戳表示
        "interval": interval, # 时间间隔，可以是1d（每日）、1wk（每周）、1mo（每月）
        "events": events, # 事件类型，可以是history（历史数据）、div（分红）、split（拆股）
        "includeAdjustedClose": "true" # 是否包含调整后的收盘价
    }
    response = requests.get(url, headers=headers, params=params)
    content = response.content
    csv = str(content)[2:-1]
    # 2. convert string to csv
    csv = csv.replace('\\t', ',').replace('\\n', '\n')
    if save_data:
        save_path = os.path.join(cwd, 'Data', data_type, f'{data_name}.csv')
        print(csv, file=open(save_path, 'w'))


get_data('Stocks', 'Apple', "1420066800", "1677625200", save_data=True)