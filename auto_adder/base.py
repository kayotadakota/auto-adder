import aiohttp
import logging
from requests import Session
from datetime import date


class Base():

    def __init__(self, name, asynchronous=False):
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

        if asynchronous:
            self.session = aiohttp.ClientSession()
        else:
            self.session = Session()

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
