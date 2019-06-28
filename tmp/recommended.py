# -*- coding: utf-8 -*-
# __author__ = "The Proud Soul"  1539688450@qq.com
# Date: 2019-06-01  Python: 3.7

import requests, tools


def crawl_recommended_by_ids(ids):
    result = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.meituan.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3803.0 Safari/537.36 Edg/76.0.176.1'
    }
    for Id in ids:
        url = 'https://www.meituan.com/meishi/' + str(Id) + '/'
        data = requests.get(url=url, headers=headers)
        if data.url == url:
            # 提取有效区域
            data = re.search(r'"recommended":(.*?),"crumbNav":', data.text, flags=re.DOTALL)
            data = json.loads(data.group(1))

            recommended = [Id]
            for x in data:
                recommended.append(x.get('name'))
                recommended.append(x.get('price'))

            result.append(recommended)
        else:
            return data
            print(data.url)
            print(data.history)

    return result
