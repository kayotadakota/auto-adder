import yaml
import asyncio
import aiohttp

from auto_adder.publishers.async_kakao_webtoon import AsyncKakaoWebtoon
from auto_adder.publishers.async_naver import AsyncNaver

from questionary import select


async def main(answer):

    with open('../proxies.yaml', 'r') as file:
            data = yaml.safe_load(file)

    PROXIES = data.get('proxies')

    if answer == 'KakaoWebtoon':

        session = aiohttp.ClientSession()
        publisher = AsyncKakaoWebtoon(session, proxy=PROXIES, retry=50)
        await publisher.collect()
        await session.close()
        await asyncio.sleep(1)

    elif answer == 'Naver':

        session = aiohttp.ClientSession()
        publisher = AsyncNaver(session, proxy=PROXIES, retry=50)
        await publisher.collect()
        await session.close()
        await asyncio.sleep(1)

    elif answer == 'KakaoNaver':
        
        session = aiohttp.ClientSession()
        naver = AsyncNaver(session, proxy=PROXIES, retry=50)
        kakao = AsyncKakaoWebtoon(session, proxy=PROXIES, retry=50)

        await asyncio.gather(
            naver.collect(),
            kakao.collect()
        )

        await session.close()
        await asyncio.sleep(1)


if __name__ == '__main__':

    answer = select(
        'Choose a publisher: ',
        choices=[
            'KakaoWebtoon',
            'Naver',
            'KakaoNaver'
        ]
    ).ask()

    asyncio.run(main(answer))
