import json
import re

import requests
from pypinyin import pinyin

from tools import gen_request_url_string


class GetCityInfo:
    def __init__(self, city_name):
        self.city_name = city_name
        self.city_acronym = "".join([i[0][0] for i in pinyin(self.city_name)])
        self.cityInfo, self.food_list = self.get_data()
        self.categories, self.areas = self.get_food_distribution(self.cityInfo['id'])

    def get_food_distribution(self, city_id):
        url = 'https://meishi.meituan.com/i/?'
        request_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'meishi.meituan.com',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.12 Mobile Safari/537.36'
        }
        query_string_parameters = {
            'ci': city_id
        }
        response = requests.get(url=gen_request_url_string(url, query_string_parameters), headers=request_headers)
        # 提取有效区域
        categories = json.loads(re.search(r'"categoryList":(.*?),"areaList', response.text, flags=re.DOTALL).group(1))
        areaList = json.loads(re.search(r'"areaList":(.*?),"areaObj":', response.text, flags=re.DOTALL).group(1))
        line_list = json.loads(re.search(r'"lineList":(.*?),"lineObj":', response.text, flags=re.DOTALL).group(1))
        line_obj = json.loads(re.search(r'"lineObj":(.*?),"stationList":', response.text, flags=re.DOTALL).group(1))
        for line in line_list:
            line['lineObj'] = line_obj[str(line['id'])]
        return categories, line_list

    def get_data(self):
        url_format = 'https://{city}.meituan.com/meishi/'
        headers = {
            #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            #         'Accept-Encoding': 'gzip, deflate, br',
            #         'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
            #         'Cache-Control': 'max-age=0',
            #         'Connection': 'keep-alive',
            #         'Host': 'gz.meituan.com',
            #         'Sec-Fetch-Site':'none',
            #         'Sec-Fetch-Mode': 'navigate',
            #         'Sec-Fetch-User': '?1',
            #         'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.12 Safari/537.36 Edg/76.0.182.6'
        }
        response = requests.get(url=url_format.format(city=self.city_acronym), headers=headers)
        city_info = json.loads(re.search(r'"currentCity":(.*?)}</script>', response.text, flags=re.DOTALL).group(1))
        #cates = json.loads(re.search(r',"filters":{"cates":(.*?),"areas":', response.text, flags=re.DOTALL).group(1))
        #areas = json.loads(re.search(r'],"areas":(.*?),"dinnerCountsAttr":', response.text, flags=re.DOTALL).group(1))
        #     totalCounts = int(re.search(r'"poiLists":{"totalCounts":(.*?),"poiInfos"', response.text, flags=re.DOTALL).group(1))
        food_list = json.loads(re.search(r',"poiInfos":(.*?)},"comHeader":', response.text, flags=re.DOTALL).group(1))
        return city_info, food_list


if __name__ == '__main__':
    city = input(r'请输入城市名字(如广州)：')
    tmp = GetCityInfo(city)
    print(tmp.cityInfo)
    print(tmp.categories)  # url=‘http://gz.meituan.com/meishi/c'+str(id)
    print(tmp.areas)  # url=‘http://gz.meituan.com/meishi/b’+str(id)
    print(tmp.food_list)
