import requests
import re
import json
import random
from datetime import datetime
from urllib.parse import urlencode, urlparse, parse_qs

# 原网站上的 url
# url = "https://jc.zhcw.com/port/client_json.php?callback=jQuery1122046489609481808847_1738207754736&transactionType=10001001&lotteryId=281&issueCount=100&startIssue=&endIssue=&startDate=&endDate=&type=0&pageNum=1&pageSize=100&tt=0.24824259101443524&_=1738207754739"
url = 'https://jc.zhcw.com/port/client_json.php?{}'

params = {
    "callback": "jQuery1122046489609481808847_1738207754736",
    "transactionType": 10001001,
    # 超级大乐透
    "lotteryId": 281,
    # 最近多少期
    "issueCount": 100,
    "type": 0,
    "pageNum": 1,
    "pageSize": 100,
    "tt": random.random(),
    "_": int(datetime.now().timestamp())
}

def get_result():
    """
    查询彩票的开奖结果
    :return:
    """
    fmt_url = url.format(urlencode(params))
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=9c63041l5r8fjht12vuu4hsn97; Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1737965883; HMACCOUNT=B0EC474093EA1D6E; Hm_lvt_12e4883fd1649d006e3ae22a39f97330=1737965883; _gid=GA1.2.1669990138.1738158029; _ga_9FDP3NWFMS=GS1.1.1738207684.4.1.1738207755.0.0.0; Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1738207756; Hm_lpvt_12e4883fd1649d006e3ae22a39f97330=1738207756; _ga=GA1.2.1718549002.1737965883',
        'Referer': 'https://www.zhcw.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", fmt_url, headers=headers, data=payload)
    text = response.text
    # 使用正则提取 JSON 部分（去掉 JSONP 的包装函数）
    match = re.match(r'^[^\(]*\((.*)\)[^\)]*$', text)
    if match:
        # 提取 JSON 部分
        json_data = match.group(1)
        # 解析 JSON 数据
        parsed_data = json.loads(json_data)
        return json.dumps(parsed_data, indent=4, ensure_ascii=False)
    else:
        return {}

def write_result(result, file_name):
    """
    写入文件
    :param file_name:
    :param result:
    :return:
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(result)

def analysis(res_list):
    """
    数据分析
    :param res_list:
    :return:
    """
    return res_list


def main():
    """
    主函数
    :return:
    """
    result = get_result()
    write_result(result, 'result.json')

    res_data = json.loads(result).get('data')
    res_list = [
        [item.get('frontWinningNum'), item.get('backWinningNum')]
        for item in res_data
    ]
    res_list.reverse()
    write_result(json.dumps(res_list, indent=4, ensure_ascii=False), 'ball_result.json')
    return analysis(res_list)

main()



