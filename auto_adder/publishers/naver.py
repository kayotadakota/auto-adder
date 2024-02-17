from auto_adder.base import Base
from auto_adder.constants import (
    NAVER_GET_UPDATE_HEADERS,
    NAVER_GET_UPDATE_URL,
    NAVER_DOWNLOAD_IMAGE_HEADERS,
)

from auto_adder.utils import translate, image_to_base64


class Naver(Base):
    

    def __init__(self):
        super().__init__('Naver')
        self.update = None


    def _get_update(self):
        
        try:
            self.logger.info('Fetching an update...')
            response = self.session.get(NAVER_GET_UPDATE_URL, headers=NAVER_GET_UPDATE_HEADERS)

            if response.status_code == 200:
                self.logger.info('Update received.')
                self.update = response.json()
            else:
                self.logger.error(f'Bad status code: {response.status_code}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    def _fetch_cover(self, title, cover_url):
        
        try:
            response = self.session.get(cover_url, headers=NAVER_DOWNLOAD_IMAGE_HEADERS)

            if response.status_code != 403:
                self.logger.info(f'Fetching the cover for {title}...')
                img_binary = response.content
                self.logger.info(f'The cover is fetched.')
                return image_to_base64(img_binary)
            else:
                raise Exception('Could not get the cover.')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')

    
    def _get_titles_info(self):
        titles_list = self.update.get('titleList')

        if not titles_list:
            raise Exception('Title list is empty.')
        
        self.logger.info('Collecting info...')
        for title in titles_list:

            if not title.get('openToday'):
                break

            self.output['another_name'] = title.get('titleName')

            if title.get('adult'):
                self.output['age_limit'] = 1
            else:
                self.output['age_limit'] = 0

            en, ru = translate(self.output['another_name'])
            self.output['secondary_name'] = en.capitalize()
            self.output['main_name'] = ru.capitalize()

            id = title.get('titleId')
            self.output['original_link'] = f'https://comic.naver.com/webtoon/list?titleId={id}'

            cover_url = title.get('thumbnailUrl')
            cover = self._fetch_cover(self.output['another_name'], cover_url)
            self.output['cover'] = 'data:image/jpeg;base64,' + cover

            self.logger.info('Info file is ready.')
            self.output_list.append(self.output)

    
    def collect(self):
        '''Aggregating together all the steps to get titles info'''

        self._get_update()
        self._get_titles_info()
