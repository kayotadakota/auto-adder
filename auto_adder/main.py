import os
import sys
import logging
import requests

from auto_adder.publishers.kakao_webtoon import KakaoWebtoon
from auto_adder.publishers.naver import Naver
from constants import (
    REMANGA_LOGIN_URL,
    REMANGA_LOGIN_HEADERS,
    REMANGA_LOGIN_PAYLOAD,
    REMANGA_ADD_NEW_TITLE_URL,
    REMANGA_ADD_NEW_TITLE_HEADERS,
    REMANGA_PREFLIGHT_LOGIN_HEADERS,
    REMANGA_PREFLIGHT_ADD_TITLE_HEADERS,
)

from questionary import select


def send_preflight_request(session, url, headers):
    logging.info('Sending preflight request...')
    res = session.options(url, headers=headers)

    if res.status_code == 200:
        logging.info('Response status code is 200.')
        return True
    else:
        logging.error(f'Bad status code: {res.status_code}')
        return False


def login(session, proxy=None) -> dict:

    REMANGA_LOGIN_PAYLOAD['password'] = os.environ.get('REMANGA_PASS')
    REMANGA_LOGIN_PAYLOAD['user'] = os.environ.get('REMANGA_USER')
 
    try:
        response = session.post(
            REMANGA_LOGIN_URL,
            headers=REMANGA_LOGIN_HEADERS,
            json=REMANGA_LOGIN_PAYLOAD,
            proxies=proxy,
            timeout=3
        )

        if response.status_code == 200:
            data = response.json()
            user_info = {}

            try:
                access_token = data.get('content').get('access_token')
                user_info['access_token'] = access_token

                publisher_id = data.get('content').get('publishers')[0].get('id')
                user_info['publisher_id'] = publisher_id

            except TypeError as ex:
                logging.error(f'Missing value: {ex}')

            if user_info:
                logging.info('User info successfully received.')
                return user_info
            else:
                logging.warning('User info is not received.')
        else:
            logging.error(f'Bad status code: {response.status_code}')
    except Exception as ex:
        logging.error(f'Unexpected error: {ex}')


def add_new_title(session, title_info, access_token: str):

    content_length = sys.getsizeof(title_info)
    name = title_info.get('another_name')

    if not title_info:
        raise Exception('Title info is missing.')
    
    REMANGA_ADD_NEW_TITLE_HEADERS['Authorization'] = 'bearer ' + access_token
    REMANGA_ADD_NEW_TITLE_HEADERS['Content-Length'] = str(content_length)

    try:
        logging.info('Sending data to the server...')
        res = session.post(
            REMANGA_ADD_NEW_TITLE_URL,
            headers=REMANGA_ADD_NEW_TITLE_HEADERS,
            json=title_info
        )

        if res.status_code == 204:
            logging.info(f'The title {name} was successfully added.')
            
        elif res.status_code == 400:
            data = res.json()
            msg = data.get('msg').get('secondary_name')[0].get('message')
            logging.info(f'{msg}')
        else:
            logging.warning(f'Unexpected status code: {res.status_code}')
    except Exception as ex:
        logging.error(f'Unexpected error: {ex}')


def main():

    logging.basicConfig(level=logging.INFO)

    answer = select(
        'Choose a publisher: ',
        choices=[
            'KakaoWebtoon',
            'Naver'
        ]
    ).ask()

    if answer == 'KakaoWebtoon':
        publisher = KakaoWebtoon()
        publisher.collect()
    elif answer == 'Naver':
        publisher = Naver()
        publisher.collect()

    with requests.Session() as session:

        if send_preflight_request(session, REMANGA_LOGIN_URL, REMANGA_PREFLIGHT_LOGIN_HEADERS):
            user_info = login(session)
            access_token = user_info.get('access_token')

            if access_token:

                for title in publisher.output_list:

                    if send_preflight_request(session, REMANGA_ADD_NEW_TITLE_URL, REMANGA_PREFLIGHT_ADD_TITLE_HEADERS):
                        add_new_title(session, title, access_token)
                    else:
                        logging.error('Preflight add title request has failed.')
            else:
                logging.error('Access token is missing.')
        else:
            logging.error('Preflight login request has failed.')

if __name__ == '__main__':
    main()