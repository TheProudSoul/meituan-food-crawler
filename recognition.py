import time
import asyncio
from pyppeteer import launch
import os

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
        await page.screenshot({'path': './example.png', 'clip': bb})

        # print(html)
        # src = re.search(r'src="blob:(.*?)">', html, flags=re.DOTALL).group(1)
        # print(src)

        #    print(src)
        #     await page.type('input.image__imageInput___2SPQH','pytn')
        # 点击验证按钮
        # await page.click('input#yodaImgCodeSure')
        await browser.close()

