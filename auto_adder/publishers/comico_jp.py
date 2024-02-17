import time
import requests
import hashlib
import json


def send_preflight_request(session):
    url = 'https://api.comico.jp/menu/all_comic/new_release'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
        'Access-Control-Request-Headers': 'x-comico-check-sum, x-comico-client-accept-mature,x-comico-client-immutable-uid,x-comico-client-os,x-comico-client-platform,x-comico-client-store,x-comico-request-time,x-comico-timezone-id',
        'Access-Control-Request-Method': 'GET',
        'Connection': 'keep-alive',
        'Host': 'api.comico.jp',
        'Origin': 'https://www.comico.jp',
        'Referer': 'https://www.comico.jp/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        response = session.options(url, headers=headers)
        
        if response.status_code == 200:
            print('Preflight request succeeded.')
            return True
        else:
            print(f'Bad status code: {response.status_code}') 
    except Exception as ex:
        print(f'Unexpected error: {ex}')


def get_new_releases(session):
    url = 'https://api.comico.jp/menu/all_comic/new_release'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ja-JP',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.1.1304431611.1707291466; NNB=XMALMBCLGPBWK; _ga_EPMDN56VX3=GS1.1.1708160362.19.1.1708161298.0.0.808538751',
        'Host': 'api.comico.jp',
        'Origin': 'https://www.comico.jp',
        'Referer': 'https://www.comico.jp/',
        'Sec-Ch-Ua': 'Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Comico-Client-Accept-Mature': 'Y',
        'X-Comico-Client-Immutable-Uid': '79.165.171.225',
        'X-Comico-Client-Os': 'other',
        'X-Comico-Client-Platform': 'web',
        'X-Comico-Client-Store': 'other',
        'X-Comico-Request-Time': str(int(time.time())),
        'X-Comico-Timezone-Id': 'Europe/Moscow',
    }

    checksum = genereta_checksum()
    headers['X-Comico-Check-Sum'] = checksum

    try:
        response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            print('New releases received.')
            return response.json()
        else:
            print(f'Bad status code: {response.status_code}') 
    except Exception as ex:
        print(f'Unexpected error: {ex}')


def genereta_checksum():
    headers = {
        "X-comico-client-os": "other",
        "X-comico-client-store": "other",
        "X-comico-request-time": str(int(time.time())),
        'X-Comico-Check-Sum': None,
        "X-comico-timezone-id": "Europe/Moscow",
        "Accept-Language": "ja-JP",
        "X-comico-client-immutable-uid": "79.165.171.225",
        "X-comico-client-platform": "web",
        "X-comico-client-accept-mature": "Y",
    }
    concatenated_string = ''

    for header, value in sorted(headers.items()):
        concatenated_string += f"{header}:{value}\n"

    checksum = hashlib.sha256(concatenated_string.encode()).hexdigest()
    return checksum

with requests.Session() as session:
    print(send_preflight_request(session))
    data = get_new_releases(session)
    print(data)





