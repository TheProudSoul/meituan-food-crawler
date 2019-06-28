import json

import requests


class GetRecommended:
    def __init__(self, shop_id):
        self.shop_id = shop_id

    def get_data(self):
        url = "https://meishi.meituan.com/i/api/dish/poi"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://meishi.meituan.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        payload = {
            "app": "",
            "optimusCode": "10",
            "partner": "126",
            "platform": "3",
            "poiId": self.shop_id,
            "riskLevel": "1",
            "uuid": "1f43caa5-eb7d-46bc-ae31-9485eb28d9dd",
            "version": "8.3.3"
        }
        tmp = requests.post(url=url, headers=headers, data=json.dumps(payload))
        return json.loads(tmp.text)['data']['list']


if __name__ == '__main__':
    # p_id = input('请输入餐馆id：')
    p_id = 6122882
    print(GetRecommended(p_id).get_data())
