import hashlib
import json

import requests


class TmpObj:
    def __init__(self):
        self.value = None


class Rsp:
    def __init__(self):
        self.ret_code = -1
        self.cust_val = 0.0
        self.err_msg = "succ"
        self.pred_rsp = TmpObj()

    def ParseJsonRsp(self, rsp_data):
        if rsp_data is None:
            self.err_msg = "http request failed, get rsp Nil data"
            return
        jrsp = json.loads(rsp_data)
        self.ret_code = int(jrsp["RetCode"])
        self.err_msg = jrsp["ErrMsg"]
        self.request_id = jrsp["RequestId"]
        if self.ret_code == 0:
            rslt_data = jrsp["RspData"]
            if rslt_data is not None and rslt_data != "":
                jrsp_ext = json.loads(rslt_data)
                if "cust_val" in jrsp_ext:
                    data = jrsp_ext["cust_val"]
                    self.cust_val = float(data)
                if "result" in jrsp_ext:
                    data = jrsp_ext["result"]
                    self.pred_rsp.value = data


def HttpRequest(url, body_data, img_data=""):
    rsp = CallRecognizeApi()
    post_data = body_data
    files = {
        'img_data': ('img_data', img_data)
    }
    header = {
        'User-Agent': 'Mozilla/5.0',
    }
    rsp_data = requests.post(url, post_data, files=files, headers=header)
    rsp.ParseJsonRsp(rsp_data.text)
    return rsp


def calc_sign(pd_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


class CallRecognizeApi:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.pd_id = "112991"  # 用户中心页可以查询到pd信息
        self.pd_key = "6yvCHmyy+G8OAv1fsnVXWVcSRd86xu7R"
        self.app_id = "312991"  # 开发者分成用的账号，在开发者中心可以查询到
        self.app_key = "p8f6nh8TzzRreDK9WuFQIo5QsJUPpPr/"
        # 识别类型，
        # 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
        self.pred_type = "30400"

    def call_recognize_api(self):
        file_name = self.timestamp + ".png"
        with open(file_name, "rb") as f:
            img_data = f.read()

        sign = calc_sign(self.pd_id, self.pd_key, self.timestamp)
        param = {
            "user_id": self.pd_id,
            "timestamp": self.timestamp,
            "sign": sign,
            "predict_type": self.pred_type,
            "up_type": "mt"
        }
        if self.app_id != "":
            #
            asign = calc_sign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = "http://pred.fateadm.com" + "/api/capreg"
        files = img_data
        rsp = HttpRequest(url, param, files)
        return rsp.pred_rsp.value
