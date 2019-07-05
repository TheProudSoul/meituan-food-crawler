import asyncio
from pyppeteer import launch
import pytesseract
from PIL import Image


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setViewport({'width': 1080, 'height': 720})

    await page.goto('https://verify.meituan.com/v2/app/general_page?action=spiderindefence&requestCode=25393170e12740c3b090bc2b728ce154&platform=3&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fmeishi.meituan.com%252Fi%252F%253Fci%253D20%2526stid_b%253D1%2526cevent%253Dimt%25252Fhomepage%25252Fcategory1%25252F1&theme=meituan')
    await asyncio.sleep(10)

    # while not await page.querySelector('img#yodaImgCode'):
    #     pass
    ele = await page.querySelector('img#yodaImgCode')
    bb = await ele.boundingBox()
    bb['x']+=1.55*bb.get('width')
    bb['y']+=1.4*bb.get('height')
    await page.screenshot({'path': './example.png','clip':bb})
    image = Image.open('example.png')
    code = pytesseract.image_to_string(image)
    print(code)
    # print(html)
    # src = re.search(r'src="blob:(.*?)">', html, flags=re.DOTALL).group(1)
    # print(src)

#    print(src)
#     await page.type('input.image__imageInput___2SPQH','pytn')
    # 点击验证按钮
    # await page.click('input#yodaImgCodeSure')
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())