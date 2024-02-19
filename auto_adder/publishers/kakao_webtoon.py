from datetime import date, timedelta
from urllib.parse import quote

from auto_adder.base import Base
from auto_adder.constants import (
    GET_UPDATE_KAKAO_WEBTOON_URL,
    GET_UPDATE_KAKAO_WEBTOON_HEADERS,
    SEARCH_ON_KAKAO_PAGE_URL,
    SEARCH_ONA_KAKAO_PAGE_HEADERS,
    SEARCH_ON_KAKAO_PAGE_PAYLOAD,
    GET_TITLE_INFO_URL,
    GET_TITLE_INFO_HEADERS,
    GET_TITLE_INFO_PAYLOAD,
    DOWNLOAD_COVER_HEADERS,
)

from auto_adder.utils import translate, image_to_base64


class KakaoWebtoon(Base):


    def __init__(self):
        super().__init__('KakaoWebtoon')
        self.update = None
        self.new_titles = []
        self.new_titles_ids = []
        self.new_titles_info = []
    

    def get_update(self):
        try:
            self.logger.info('Fetching an update...')
            response = self.session.get(
                GET_UPDATE_KAKAO_WEBTOON_URL,
                headers=GET_UPDATE_KAKAO_WEBTOON_HEADERS
            )
            
            if response.status_code == 200:
                self.logger.info('Update received.')
                self.update = response.json()
            
            else:
                self.logger.error(f'Bad status code: {response.status_code}')
        
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


    def check_date(self, raw_date: str) -> bool:
        today = date.today()
        year = today.year
        one_day = timedelta(days=1)
        tomorrow = today + one_day
        iso_date_format = '-'.join([str(year)] + raw_date.split('.'))
        target_date = date.fromisoformat(iso_date_format)

        return tomorrow == target_date
    

    def search_on_kakao_page(self, test=None):
        '''To test the function set the test parameter to a list of titles'''

        if test:
            self.new_titles = test

        for title in self.new_titles:

            encoded_title = quote(title)
            SEARCH_ONA_KAKAO_PAGE_HEADERS['Referer'] = f"https://page.kakao.com/search/result?keyword={encoded_title}&categoryUid=10"
            SEARCH_ON_KAKAO_PAGE_PAYLOAD['variables']['input']['keyword'] = title

            try:
                response = self.session.post(
                    SEARCH_ON_KAKAO_PAGE_URL,
                    headers=SEARCH_ONA_KAKAO_PAGE_HEADERS,
                    json=SEARCH_ON_KAKAO_PAGE_PAYLOAD
                )

                if response.status_code == 200:
                    data = response.json()
                    search_results = data.get('data').get('searchKeyword').get('list')

                    if search_results:
                        self.logger.info('Searching for matching in the search results...')

                        for result in search_results:
                            name = result.get('eventLog').get('eventMeta').get('name')

                            if name == title:
                                id = result.get('eventLog').get('eventMeta').get('id')
                                self.new_titles_ids.append(id)
                                break
                    else:
                        self.logger.warning(f'Couldn\'t find anything based on {title} request.')
                else:
                    self.logger.error(f'Bad status code: {response.status_code}')
            except Exception as ex:
                self.logger.error(f'Unexpected error: {ex}')

    
    def _fetch_cover(self, title: str, cover_url: str):

        try:
            response = self.session.get(cover_url, headers=DOWNLOAD_COVER_HEADERS)

            if response.status_code == 200:
                self.logger.info(f'Fetching the cover for {title}...')
                img_binary = response.content
                self.logger.info(f'The cover is fetched.')
                return image_to_base64(img_binary)
            else:
                raise Exception('Could not fetch the cover.')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


    def get_titles_info(self):
        self.logger.info('Collecting titles info...')

        for id in self.new_titles_ids:
            
            GET_TITLE_INFO_HEADERS['Referer'] = f'https://page.kakao.com/content/{id}'
            GET_TITLE_INFO_PAYLOAD['variables']['seriesId'] = id

            try:
                response = self.session.post(
                    GET_TITLE_INFO_URL,
                    headers=GET_TITLE_INFO_HEADERS,
                    json=GET_TITLE_INFO_PAYLOAD
                )

                if response.status_code == 200:

                    data = response.json()
                    content = data.get('data').get('contentHomeOverview').get('content')

                    self.output['another_name'] = content.get('title')

                    age = content.get('ageGrade')
                    if age.lower() == 'nineteen':
                        self.output['age_limit'] = 1
                    else:
                        self.output['age_limit'] = 0

                    self.output['original_link'] = f'https://page.kakao.com/content/{id}'

                    en, ru = translate(self.output['another_name'])
                    self.output['secondary_name'] = en.capitalize()
                    self.output['main_name'] = ru.capitalize()

                    cover_url = 'https:' + content.get('thumbnail')
                    cover = self._fetch_cover(self.output['another_name'], cover_url)
                    self.output['cover'] = 'data:image/jpeg;base64,' + cover

                    self.output_list.append(self.output)
                    self.logger.info('Info file is ready.')

                else:
                    self.logger.error(f'Bad status code: {response.status_code}')
            except Exception as ex:
                self.logger.error(f'Unexpected error: {ex}')

        self.logger.info(f'{len(self.output_list)} titles info collected.')

    
    def collect(self, test=None):
        '''Aggregating together all the steps to get titles info'''

        if test:
            self.search_on_kakao_page(test=test)
            self.get_titles_info()

        else:
            self.get_update()
            self.get_new()
            self.search_on_kakao_page()
            self.get_titles_info()

