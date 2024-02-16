import base64
from deep_translator import GoogleTranslator


def translate(text: str) -> tuple:
    en = GoogleTranslator(source='korean', target='english').translate(text)
    ru = GoogleTranslator(source='korean', target='russian').translate(text)
    return (en, ru)


def image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as image:
        img_binary = image.read()
        img_base64 = base64.b64encode(img_binary)
        img_base64_str = img_base64.decode('utf-8')

    return img_base64_str