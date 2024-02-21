import yaml
import unittest
import requests

from auto_adder.constants import (
    NAVER_GET_UPDATE_URL,
    NAVER_GET_UPDATE_HEADERS,
    GET_UPDATE_KAKAO_WEBTOON_URL,
    GET_UPDATE_KAKAO_WEBTOON_HEADERS,
)


class TestProxies(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestProxies, self).__init__(*args, **kwargs)

        with open('proxies.yaml', 'r') as file:
            data = yaml.safe_load(file)

        self.proxies = data.get('proxies')


    def test_proxies_on_naver(self):
        '''Check if there is a proxy that has been banned on the Naver's server'''
        
        for proxy in self.proxies:
            
            response = requests.get(
                NAVER_GET_UPDATE_URL,
                headers=NAVER_GET_UPDATE_HEADERS,
                proxies={'http': proxy, 'https': proxy}
            )
            self.assertEqual(response.status_code, 200)

    
    def test_proxies_on_kakao(self):
        '''Check if there is a proxy that has been banned on the Kakao's server'''
        
        for proxy in self.proxies:
            
            response = requests.get(
                GET_UPDATE_KAKAO_WEBTOON_URL,
                headers=GET_UPDATE_KAKAO_WEBTOON_HEADERS,
                proxies={'http': proxy, 'https': proxy}
            )
            self.assertEqual(response.status_code, 200)


unittest.main()