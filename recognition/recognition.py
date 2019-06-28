import time
import asyncio
from pyppeteer import launch
import hashlib

from meituan.recognize import FateadmApi
from recognition.call_recognize_api import CallRecognizeApi


def CalcSign(pd_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


class Recognition:
    def __init__(self, url):
        self.url = url
        self.timestamp = str(int(time.time()))
        self.file_name = self.timestamp + ".png"

    async def get_pic(self):
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.setViewport({'width': 1080, 'height': 720})

        await page.goto(self.url)
        await asyncio.sleep(10)

        # while not await page.querySelector('img#yodaImgCode'):
        #     pass
        ele = await page.querySelector('img#yodaImgCode')
        bb = await ele.boundingBox()
        bb['x'] += 1.55 * bb.get('width')
        bb['y'] += 1.4 * bb.get('height')
        await page.screenshot({'path': './'+self.timestamp+'.png', 'clip': bb})
        result = CallRecognizeApi(self.timestamp).call_recognize_api

        # 获取输入框

        # 点击验证按钮
        await page.click('input#yodaImgCodeSure')
        await browser.close()

