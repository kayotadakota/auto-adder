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
