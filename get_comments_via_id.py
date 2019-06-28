import json
import re
import time

import requests

import tools


class GetComments:
    def __init__(self, shop_id):
        self.shop_id = shop_id

        self.get_data()

    @staticmethod
    def decode_time(time_stamp):
        """13位 解码时间
        """
        temp = float(int(time_stamp) / 1000)
        time_array = time.localtime(temp)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

    def process_comments(self, raw_data):
        data = json.loads(raw_data)['data']['comments']
        comments = []
        for comment in data:
            comments.append({
                'store_id': self.shop_id,
                'reviewId': comment.get('reviewId'),
                'time': self.decode_time(comment.get('commentTime')),
                'comment': comment.get('comment'),
                'star': comment.get('star')
            })

        return comments

    def get_data(self):
        url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?'
        # uuid=1f43caa5-eb7d-46bc-ae31-9485eb28d9dd&platform=1&partner=126&originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F5548637%2F&riskLevel=1&optimusCode=1&id=5548637&userId=&offset=0&pageSize=10&sortType=1
        header = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'www.meituan.com',
            'Referer': 'https://www.meituan.com/meishi/' + str(self.shop_id) + '/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        query_string_parameters = {
            'uuid': '1f43caa5-eb7d-46bc-ae31-9485eb28d9dd',
            'platform': 1,
            'partner': 126,
            'originUrl': 'https://www.meituan.com/meishi/' + str(self.shop_id) + '/',
            'riskLevel': 1,
            'optimusCode': 1,
            'id': self.shop_id,
            'userId': '',
            'offset': 0,
            'pageSize': 100,
            'sortType': 1,
        }

        first_request = requests.get(url=tools.gen_request_url_string(url, query_string_parameters), headers=header)
        result = self.process_comments(first_request.text)
        total = int(re.search(r'"total":(.*?)}}', first_request.text).group(1))

        for x in range(1, int(total / 100)):
            query_string_parameters['offset'] += 100
            response = requests.get(url=tools.gen_request_url_string(url, query_string_parameters), headers=header)
            tmp = self.process_comments(response.text)
            print(tmp)
            result.extend(tmp)

        return result


if __name__ == '__main__':
    p_id = input('请输入餐馆id：')
    # p_id = 6122882
    GetComments(p_id)
