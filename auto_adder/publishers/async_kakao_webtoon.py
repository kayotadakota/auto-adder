import asyncio
import aiohttp

from random import choice
from datetime import date, timedelta
from urllib.parse import quote

from auto_adder.base import Base
from auto_adder.constants import (
    GET_UPDATE_KAKAO_WEBTOON_URL,
    GET_UPDATE_KAKAO_WEBTOON_HEADERS,
    SEARCH_ON_KAKAO_PAGE_URL,
    SEARCH_ON_KAKAO_PAGE_HEADERS,
    SEARCH_ON_KAKAO_PAGE_PAYLOAD,
    GET_TITLE_INFO_URL,
    GET_TITLE_INFO_HEADERS,
    GET_TITLE_INFO_PAYLOAD,
    DOWNLOAD_COVER_HEADERS,
    REMANGA_LOGIN_URL,
    REMANGA_PREFLIGHT_LOGIN_HEADERS,
    REMANGA_ADD_NEW_TITLE_URL,
    REMANGA_PREFLIGHT_ADD_TITLE_HEADERS,
)

from auto_adder.utils import async_translate, image_to_base64


class AsyncKakaoWebtoon(Base):


    def __init__(self, session, **kwargs):
        super().__init__('KakaoWebtoon', session, **kwargs)
        self.update = None
        self.new_titles = []
        self.new_titles_ids = []
    

    async def get_update(self):

        proxy = choice(self.proxies)

        try:
            self.logger.info('Fetching an update...')
            async with self.session.get(
                GET_UPDATE_KAKAO_WEBTOON_URL,
                headers=GET_UPDATE_KAKAO_WEBTOON_HEADERS,
                proxy=proxy
            ) as response:
            
                if response.status == 200:
                    self.logger.info('Update received.')
                    self.update = await response.json()
            
                else:
                    self.logger.error(f'Bad status code: {response.status}, proxy: {proxy}')
        
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    def get_new(self):
        self.logger.info('Looking for new titles...')
        title_list = self.update.get('data')[0].get('cardGroups')[0].get('cards')

        if not title_list:
            raise Exception('Titles list is empty.')
        
        for title in title_list:
            raw_date = title['additional']['label']

            try:
                if not self.check_date(raw_date):
                    break
            except ValueError:
                break

            self.new_titles.append(title['content']['title'])

        self.logger.info(f'{len(self.new_titles)} new titles were found.')


    async def _wait_for_update(self):
        self.logger.info('Waiting for an update...')

        if not isinstance(self.retry, int) and self.retry > 0:
            self.logger.error('Retry value must be an int type and greater than 0.')

        while self.retry > 0:

            await self.get_update()
            self.get_new()

            if not self.new_titles:
                self.retry -= 1
                await asyncio.sleep(0.5)
                continue

            return
        
        self.logger.warning('Retry attemps exceeded.')


    def check_date(self, raw_date: str) -> bool:
        today = date.today()
        year = today.year
        one_day = timedelta(days=1)
        tomorrow = today + one_day
        iso_date_format = '-'.join([str(year)] + raw_date.split('.'))
        target_date = date.fromisoformat(iso_date_format)

        return tomorrow == target_date
    

    async def _search_on_kakao_page(self, title: str):

        encoded_title = quote(title)
        SEARCH_ON_KAKAO_PAGE_HEADERS['Referer'] = f"https://page.kakao.com/search/result?keyword={encoded_title}&categoryUid=10"
        SEARCH_ON_KAKAO_PAGE_PAYLOAD['variables']['input']['keyword'] = title
        proxy = choice(self.proxies) 
        
        try:
            async with self.session.post(
                SEARCH_ON_KAKAO_PAGE_URL,
                headers=SEARCH_ON_KAKAO_PAGE_HEADERS,
                json=SEARCH_ON_KAKAO_PAGE_PAYLOAD,
                proxy=proxy
            ) as response:

                if response.status == 200:
                    data = await response.json()
                    search_results = data.get('data').get('searchKeyword').get('list')

                    if search_results:
                        self.logger.info('Searching for matching in the search results...')

                        for result in search_results:
                            name = result.get('eventLog').get('eventMeta').get('name')
                            name = name.strip()

                            if name == title:
                                id = result.get('eventLog').get('eventMeta').get('id')
                                self.new_titles_ids.append(id)
                                break
                    else:
                        self.logger.warning(f'Couldn\'t find anything based on {title} request.')
                else:
                    self.logger.error(f'Bad status code: {response.status}, proxy: {proxy}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')

    
    async def _fetch_cover(self, title: str, cover_url: str):

        try:
            async with self.session.get(cover_url, headers=DOWNLOAD_COVER_HEADERS) as response:

                if response.status == 200:
                    self.logger.info(f'Fetching the cover for {title}...')
                    img_binary = await response.read()
                    self.logger.info(f'The cover is fetched.')
                    return image_to_base64(img_binary)
                else:
                    raise Exception('Could not fetch the cover.')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    async def _get_title_info(self, title_id):
        output = self.output.copy()

        GET_TITLE_INFO_HEADERS['Referer'] = f'https://page.kakao.com/content/{title_id}'
        GET_TITLE_INFO_PAYLOAD['variables']['seriesId'] = title_id
        proxy = choice(self.proxies)

        try:
            async with self.session.post(
                GET_TITLE_INFO_URL,
                headers=GET_TITLE_INFO_HEADERS,
                json=GET_TITLE_INFO_PAYLOAD,
                proxy=proxy
            ) as response:

                if response.status == 200:

                    data = await response.json()
                    content = data.get('data').get('contentHomeOverview').get('content')

                    output['another_name'] = content.get('title')

                    age = content.get('ageGrade')
                    if age.lower() == 'nineteen':
                        output['age_limit'] = 1
                    else:
                        output['age_limit'] = 0

                    output['original_link'] = f'https://page.kakao.com/content/{title_id}'

                    loop = asyncio.get_running_loop()
                    en, ru = await async_translate(loop, output['another_name'])
                    output['secondary_name'] = en.capitalize()
                    output['main_name'] = ru.capitalize()

                    cover_url = 'https:' + content.get('thumbnail')
                    cover = await self._fetch_cover(output['another_name'], cover_url)
                    output['cover'] = "data:image/png;base64," + cover

                    self.output_list.append(output)
                    self.logger.info('Info file is ready.')

                else:
                    self.logger.error(f'Bad status code: {response.status}, proxy: {proxy}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')

    
    async def collect(self, test=None):
        '''Aggregating together all the steps to get titles info'''

        if test:
            self.new_titles = test

            self.logger.info('Gathering tasks for search...')
            search_tasks = [self._search_on_kakao_page(title.strip()) for title in self.new_titles]
            await asyncio.gather(*search_tasks)
            self.logger.info('Gathered and awaited.')

            self.logger.info('Gathering tasks for info...')
            get_info_tasks = [self._get_title_info(id) for id in self.new_titles_ids]
            await asyncio.gather(*get_info_tasks)
            self.logger.info('Gathered and awaited')
        else:
            await self._wait_for_update()

            search_tasks = [self._search_on_kakao_page(title.strip()) for title in self.new_titles]
            await asyncio.gather(*search_tasks)

            get_info_tasks = [self._get_title_info(id) for id in self.new_titles_ids]
            await asyncio.gather(*get_info_tasks)

            if self.output_list:
                preflight_login = await self._send_preflight_request(REMANGA_LOGIN_URL, REMANGA_PREFLIGHT_LOGIN_HEADERS)

                if preflight_login:
                    await self._login()

                    if self.access_token:

                        for title in self.output_list:
                            preflight_add = await self._send_preflight_request(
                                REMANGA_ADD_NEW_TITLE_URL,
                                REMANGA_PREFLIGHT_ADD_TITLE_HEADERS
                            )

                            if preflight_add:
                                await self._add_new_title(title)

                            await asyncio.sleep(0.3)




                       




