# -*- coding: utf-8 -*-
# __author__ = "The Proud Soul"  1539688450@qq.com
# Date: 2019-06-01  Python: 3.7

import pandas as pd
from urllib import parse


def save_as_csv(file_name, list_name):
    tmp = pd.DataFrame(columns=list(list_name[0].keys()), data=list_name)
    # tmp.drop_duplicates()
    tmp.to_csv(file_name, encoding='gb18030')

    
def save_as_csv_without_column_keys(file_name, list_name):
    tmp = pd.DataFrame(data=list_name)
    # tmp.drop_duplicates()
    tmp.to_csv(file_name, encoding='gb18030', index=False, header=False)


def gen_request_url_string(url, parameters):
    return url + parse.urlencode(parameters)


def drag_ids_from_list(l):
    result = []
    for x in l:
        result.append(x.get('id'))

    return result
