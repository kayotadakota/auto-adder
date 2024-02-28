import asyncio

from random import choice

from auto_adder.base import Base
from auto_adder.constants import (
    NAVER_GET_UPDATE_HEADERS,
    NAVER_GET_UPDATE_URL,
    NAVER_DOWNLOAD_IMAGE_HEADERS,
    REMANGA_LOGIN_URL,
    REMANGA_PREFLIGHT_LOGIN_HEADERS,
    REMANGA_ADD_NEW_TITLE_URL,
    REMANGA_PREFLIGHT_ADD_TITLE_HEADERS,
)

from auto_adder.utils import async_translate, image_to_base64


class AsyncNaver(Base):
    

    def __init__(self, session, **kwargs):
        super().__init__('Naver', session, **kwargs)
        self.update = None
        self.titles_list = None
        self.new_titles = []


    async def _get_update(self):
        
        proxy = choice(self.proxies)

        try:
            self.logger.info('Fetching an update...')
            async with self.session.get(
                NAVER_GET_UPDATE_URL,
                headers=NAVER_GET_UPDATE_HEADERS,
                proxy=proxy
            ) as response:

                if response.status == 200:
                    self.logger.info('Update received.')
                    self.update = await response.json()
                else:
                    self.logger.error(f'Bad status code: {response.status}, proxy: {proxy}')

        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    async def _fetch_cover(self, title, cover_url):

        proxy = choice(self.proxies)
        
        try:
            async with self.session.get(
                cover_url,
                headers=NAVER_DOWNLOAD_IMAGE_HEADERS,
                proxy=proxy
            ) as response:

                if response.status != 403:
                    self.logger.info(f'Fetching the cover for {title}...')
                    img_binary = await response.read()
                    self.logger.info(f'The cover is fetched.')
                    return image_to_base64(img_binary)
                else:
                    raise Exception('Could not get the cover.')
                
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')

    
    async def _get_title_info(self, title):
        output = self.output.copy()

        output['another_name'] = title.get('titleName')

        if title.get('adult'):
            output['age_limit'] = 1
        else:
            output['age_limit'] = 0

        loop = asyncio.get_running_loop()
        en, ru = await async_translate(loop, output['another_name'])
        output['secondary_name'] = en.capitalize()
        output['main_name'] = ru.capitalize()

        id = title.get('titleId')
        output['original_link'] = f'https://comic.naver.com/webtoon/list?titleId={id}'

        cover_url = title.get('thumbnailUrl')
        cover = await self._fetch_cover(output['another_name'], cover_url)
        output['cover'] = 'data:image/png;base64,' + cover

        self.logger.info('Info file is ready.')
        self.output_list.append(output)


    async def _wait_for_update(self):
        self.logger.info('Waiting for an update...')

        if not isinstance(self.retry, int) and self.retry > 0:
            self.logger.error('Retry value must be an int type and greater than 0.')

        while self.retry > 0:

            await self._get_update()
            self.titles_list = self.update.get('titleList')

            if not self.titles_list:
                self.logger.error('Titles list is empty.')
                return
            
            if not self.titles_list[0].get('openToday'):
                self.retry -= 1
                await asyncio.sleep(0.5)
                continue

            return

        self.logger.warning('Retry attemps exceeded.')

    
    async def collect(self):
        '''Aggregating together all the steps to get titles info'''

        await self._wait_for_update()

        for title in self.titles_list:

            if not title.get('openToday'):
                break

            self.new_titles.append(title)

        self.logger.info('Collecting info...')
        get_info_tasks = [self._get_title_info(title) for title in self.new_titles]
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


