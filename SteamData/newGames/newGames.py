'''
Steam의 신작 데이터 수집
bs4를 이용한 크롤링
'''
import time
import requests
from bs4 import BeautifulSoup
import pickle


# constants
NEW_GAMES_BASE_URL = 'https://store.steampowered.com/explore/new/'
GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'

# time estimate
startTime = time.time()


# 2. 게임 id 크롤링, bs4여도 상관이 없다
payload = { 'l': 'korean' }
response = requests.get(NEW_GAMES_BASE_URL, params=payload).text
soup = BeautifulSoup(response, 'html.parser')
newGameIds = set()

for link in soup.find_all('a'):
    # get value of attribute "data-ds-appid"
    gameId = link.get('data-ds-appid')
    if gameId:
        # if a game has DLCs, game_id is like "game_id,DLC1_id,DLC2_id"
        gameId = gameId.split(',')[0]
        newGameIds.add(gameId)

newGameDetails = {}
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
for gameId in newGameIds:
    # db에 있다면 스킵 없다면 db에 추가
    cnt += 1
    if cnt % 10 == 0:
        time.sleep(11)

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
    if response['type'] != 'game':
        continue

    requestEndTime = time.time()
    print(f'{cnt}번째 게임 요청 완료, {requestEndTime - requestStartTime:.2f}초 소요')
    
    data = {}
    for key in keys:
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
    newGameDetails[gameId] = data

    parsingEndTime = time.time()
    print(f'{cnt}번째 게임 parsing 완료, {parsingEndTime - requestEndTime:.2f}초 소요')
    print(f'{cnt}번째 게임 확보 완료, {parsingEndTime - requestStartTime:.2f}초 소요')

endTime = time.time()

print(f'{endTime - startTime:.2f}초 소요')
print(f'{len(newGameDetails)}개의 게임 detail 확보')

with open(r"newGames/newGames.pkl", "wb") as f:
    pickle.dump(newGameDetails, f)

print(f'{len(requestErrorGameIds)}개의 게임 detail 확보 실패')
if requestErrorGameIds:
    with open(r"newGames/newGamesFailed.pkl", "wb") as f:
        pickle.dump(requestErrorGameIds, f)

print(f'{len(requestErrorGameIds)}개의 게임 request error occured')
