'''
Steam의 신작 데이터 수집
bs4를 이용한 크롤링
'''
import time
import requests
from bs4 import BeautifulSoup
import pickle


# constants
GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'
KEYS = [
    'name',
    'steam_appid',
    'required_age',
    'detailed_description',
    'about_the_game',
    'short_description',
    'supported_languages',
    'header_image',
    'website',
    'pc_requirements',
    'legal_notice',
    'developers',
    'publishers',
    'price_overview',
    'metacritic',
    'categories',
    'genres',
    'screenshots',
    'movies',
    'release_date',
    'background',
    'background_raw'
]

with open('topSellers/topSellersIds.pkl', 'rb') as f:
    topSellersIds = pickle.load(f)

cnt = 0
topSellersDetails = []
for gameId in topSellersIds[:100]:
    cnt += 1
    if cnt % 10 == 0:
        print(f'{cnt} 번째 요청')
        time.sleep(11)
    
    payload = { 'appids': gameId, 'l': 'korean' }
    try:
        response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()
    except Exception as e:
        print(f'Error occurred! Error: {e}')
        print(gameId)
        continue

    if not response:
        print(gameId)
        continue

    response = response[gameId]
    if response['success'] == False:
        # 한국어 지원이 안 되는 게임인 경우
        print(gameId)
        continue

    response = response.get('data')
    if response['type'] != 'game':
        print(gameId)
        continue

    data = {}
    for key in KEYS:
        # data[key] = cleanHtml(response.get(key))
        dataItem = response.get(key)
        if isinstance(dataItem, str) and dataItem[:4] != 'http':
            data[key] = BeautifulSoup(response.get(key), 'html.parser').get_text()
        elif isinstance(dataItem, dict):
            for k, v in dataItem.items():
                if isinstance(v, str) and v[:4] != 'http':
                    dataItem[k] = BeautifulSoup(v, 'html.parser').get_text()
                else:
                    dataItem[k] = v
            data[key] = dataItem
        else:
            data[key] = dataItem

    topSellersDetails.append(data)

print(f'{len(topSellersDetails)}개의 게임 detail 확보')

with open("topSellers/topSellers.pkl", "wb") as f:
    pickle.dump(topSellersDetails, f)

print(topSellersDetails)
