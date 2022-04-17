'''
지역에서 제공되지 않는 게임
ex. https://store.steampowered.com/app/653450/2/12/
한국어가 제공되지 않는 게임
'''
import pickle
import requests
from bs4 import BeautifulSoup
import time

GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'

startTime = time.time()

with open(r'userGames/allGameIds.pkl', 'rb') as f:
    allGameIds = pickle.load(f)

gameDetails = {}
requestErrorGameIds = []
keys = [
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
cnt = 0
allGameIdsIntList = list(map(int, allGameIds))
allGameIdsIntList.sort()
allGameIds = list(map(str, allGameIdsIntList))
allGameIdsNum = len(allGameIds)
for unit in range(10):
    startGameId = (allGameIdsNum // 10) * unit 
    endGameId = (allGameIdsNum // 10) * (unit + 1)
    if unit == 9:
        endGameId = allGameIdsNum

    for gameId in allGameIds[startGameId:endGameId]:
        cnt += 1
        if cnt % 10 == 0:
            time.sleep(11)

        gameId = str(gameId)
        requestStartTime = time.time()
        print(f'{cnt}번째 게임 요청 시작')
        payload = { 'appids': gameId, 'l': 'korean' }
        try:
            response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()
        except Exception as e:
            requestErrorGameIds.append(gameId)
            print(f'Error occurred! Error: {e}')
            print(gameId)
            continue
            
        if not response:
            print(gameId)
            continue
        response = response[gameId]
        if response['success'] == False:
            # 한국어 지원이 안 되는 게임인 경우
            continue

        response = response.get('data')
        requestEndTime = time.time()
        print(f'{cnt}번째 게임 요청 완료, {requestEndTime - requestStartTime:.2f}초 소요')
        if response['type'] != 'game':
            continue
        data = {}
        for key in keys:
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
        gameDetails[gameId] = data

        parsingEndTime = time.time()
        print(f'{cnt}번째 게임 parsing 완료, {parsingEndTime - requestEndTime:.2f}초 소요')
        print(f'{cnt}번째 게임 확보 완료, {parsingEndTime - requestStartTime:.2f}초 소요')

    endTime = time.time()

    print(f'{endTime - startTime:.2f}초 소요')
    print(f'{len(gameDetails)}개의 게임 detail 확보')

    with open(f"allGameDetails/allGameDetails{unit}.pkl", "wb") as f:
        pickle.dump(gameDetails, f)

    print(f'{len(requestErrorGameIds)}개의 게임 detail 확보 실패')
    with open(f"allGameDetails/allGameDetailsFailed{unit}.pkl", "wb") as f:
        pickle.dump(requestErrorGameIds, f)

    print(f'{unit} unit 완료')
