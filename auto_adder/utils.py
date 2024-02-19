import asyncio
import base64
from deep_translator import GoogleTranslator


def translate(text: str) -> tuple:
    translator = GoogleTranslator(source='korean', target='english')
    en = translator.translate(text)
    translator.target = 'ru'
    ru = translator.translate(text)
    return (en, ru)


def image_to_base64(img_binary: bytes) -> str:
    img_base64 = base64.b64encode(img_binary)
    img_base64_str = img_base64.decode('utf-8')

    return img_base64_str


async def async_translate(loop, text):
    return await loop.run_in_executor(None, translate, text)


async def main():
    loop = asyncio.get_running_loop()
    result = await async_translate(loop, '다시 한번, 빛 속으로')
    print(result)

asyncio.run(main())