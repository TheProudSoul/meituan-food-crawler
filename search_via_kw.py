import json
from urllib import parse

import requests

import tools


class GetSearchResult:
    def __init__(self, city_id, key_word):
        self.city_id = city_id
        self.key_word = key_word

    def gen_search_request_urls(self):
        url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/'+str(self.city_id)+'?'
        urls = []
        query_string_parameters = {
            'uuid': '29d923a77824412194e3.1560221341.1.0.0',  # Demo
            'userid': -1,
            'limit': 50,
            'offset': 0,
            'cateId': -1,
            'q': self.key_word
        }

        for i in range(3):
            urls.append(tools.gen_request_url_string(url, query_string_parameters))
            query_string_parameters['offset'] += 50

        return urls

    @staticmethod
    def process_search_result(raw_data):
        data = json.loads(raw_data)
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

    def get_data(self):
        url_list = self.gen_search_request_urls()
        request_header = {
            'Referer': 'https://gz.meituan.com/s/' + parse.quote(self.key_word) + '/',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/'
        }

        result = []
        for url in url_list:
            response = requests.get(url=url, headers=request_header)
            if response.url == url:
                result.extend(self.process_search_result(response.text))
            else:
                print(response.url)

        return result


if __name__ == '__main__':
    s_area = input(r'请输入搜索区域id(如广州区域为20)：')
    s_key = input(r'请输入搜索关键字：')
    print(GetSearchResult(s_area, s_key).get_data())
