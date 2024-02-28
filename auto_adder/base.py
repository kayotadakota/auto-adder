import os
import sys
import logging

from datetime import date

from auto_adder.constants import (
    REMANGA_LOGIN_URL,
    REMANGA_LOGIN_HEADERS,
    REMANGA_LOGIN_PAYLOAD,
    REMANGA_ADD_NEW_TITLE_URL,
    REMANGA_ADD_NEW_TITLE_HEADERS,
)


class Base():

    def __init__(self, name, session, proxy=None, retry=1):
        '''
        --- Set age_limit to 1 for adult titles
        --- Another name is the title original name (in Korean, Japanese etc.)
        --- Send cover in base64 format with following prefix 'data:image/jpeg;base64,'
        --- Main name is the title name in Russian
        --- Secondary name is the title name in English
        --- Publishers are the ids of remanga teams
        --- Set type to 0 for manga, 1 for manhwa, 2 for manhua, 3 for western comics etc.
        --- User message is the message for a moderator
        '''
        
        self.output = {
            'adaptation_link': '',
            'age_limit': 0,
            'anlate_link': '',
            'another_name': None,
            'categories': [6, 5],
            'cover': None,
            'genres': [9],
            'issue_year': str(date.today().year),
            'main_name': None,
            'original_link': None,
            'publishers': [12327],
            'secondary_name': None,
            'status': 1,
            'type': 1,
            'user_message': '',
        }

        self.output_list = []
        self.access_token = None
        self.proxies: list[str] = proxy
        self.retry = retry
        self.session = session

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)


    async def _send_preflight_request(self, url, headers):

        self.logger.info('Sending preflight request...')

        try:
            async with self.session.options(url, headers=headers) as response:

                if response.status == 200:
                    self.logger.info('Response status code is 200.')
                    return True
                else:
                    self.logger.warning(f'Bad status code: {response.status}')
                    return False
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    async def _login(self) -> dict:

        REMANGA_LOGIN_PAYLOAD['password'] = os.environ.get('REMANGA_PASS')
        REMANGA_LOGIN_PAYLOAD['user'] = os.environ.get('REMANGA_USER')
    
        try:

            async with self.session.post(
                REMANGA_LOGIN_URL,
                headers=REMANGA_LOGIN_HEADERS,
                json=REMANGA_LOGIN_PAYLOAD,
                timeout=3
            ) as response:

                if response.status == 200:
                    data = await response.json()

                    try:
                        token = data.get('content').get('access_token')
                        self.access_token = token

                    except TypeError as ex:
                        self.logger.error(f'Missing value: {ex}')

                    if self.access_token:
                        self.logger.info('User info successfully received.')
                    else:
                        self.logger.warning('User info is not received.')
                else:
                    self.logger.warning(f'Bad status code: {response.status}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    async def _add_new_title(self, title_info):
        '''If the content-length is specified and exceeded the actual length than
        the data would be cut down to the specified size.'''

        name = title_info.get('another_name')

        if not title_info:
            raise Exception('Title info is missing.')
        
        REMANGA_ADD_NEW_TITLE_HEADERS['Authorization'] = 'bearer ' + self.access_token

        try:
            self.logger.info('Sending data to the server...')

            async with self.session.post(
                REMANGA_ADD_NEW_TITLE_URL,
                headers=REMANGA_ADD_NEW_TITLE_HEADERS,
                json=title_info
            ) as response:

                if response.status == 204:
                    self.logger.info(f'The title {name} was successfully added.')
                    
                elif response.status == 400:
                    data = await response.json()
                    msg = data.get('msg')
                    self.logger.warning(f'{msg}')

                else:
                    self.logger.warning(f'Bad status code: {response.status}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')