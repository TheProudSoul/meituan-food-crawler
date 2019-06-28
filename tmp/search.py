# -*- coding: utf-8 -*-
# __author__ = "The Proud Soul"  1539688450@qq.com
# Date: 2019-06-01  Python: 3.7

import json
import tools
import requests
from urllib import parse


def process_search_result(s):
    data = json.loads(s)
    result = []
    for store in data['data']['searchResult']:
        result.append({
            'id': store.get('id'),
            'title': store.get('title'),
            'address': store.get('address'),
            'area_name': store.get('areaname'),
            'avg_price': store.get('avgprice'),
            'avg_score': store.get('avgscore'),
            'backCateName': store.get('backCateName'),
            'cate': store.get('cate'),
            'city': store.get('city'),
            'comments': store.get('comments'),
            'latitude': store.get('latitude'),
            'longitude': store.get('longitude')
        })

    return result


def gen_search_request_urls(kw):
    url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/20?'
    urls = []
    query_string_parameters = {
        'uuid': '29d923a77824412194e3.1560221341.1.0.0',  # Demo
        'userid': -1,
        'limit': 50,
        'offset': 0,
        'cateId': -1,
        'q': kw
    }

    for i in range(3):
        urls.append(tools.gen_request_url_string(url, query_string_parameters))
        query_string_parameters['offset'] += 50

    return urls


# 获取搜索列表
# TODO:爬取城市ID
def get_search_result():
    s_key = input(r'请输入搜索关键字(广州区域)：')
    url_list = gen_search_request_urls(s_key)
    request_header = {
        'Referer': 'https://gz.meituan.com/s/' + parse.quote(s_key) + '/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/'
    }

    result = []
    for url in url_list:
        response = requests.get(url=url, headers=request_header)
        if response.url == url:
            result.extend(process_search_result(response.text))
        else:
            print(response.url)

    return result
