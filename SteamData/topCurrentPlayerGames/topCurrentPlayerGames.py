'''
today best or current
steam 게임이 아닌 경우도 포함
'''
import requests
from bs4 import BeautifulSoup
import pickle
import time


TOP_CURRENT_GAMES_BASE_URL = 'https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics'
GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'

startTime = time.time()

payload = { 'l': 'korean' }
response = requests.get(TOP_CURRENT_GAMES_BASE_URL, params=payload).text
soup = BeautifulSoup(response, 'html.parser')
# (players(int), gameId(str))
topCurrentGameIds = []
topTodayGameIds = []
# loop for all a tags
for link in soup.find_all('tr', attrs={ 'class': 'player_count_row' }):
    # get value of attribute "data-ds-appid"
    # print(link)
    # print(link.find('span'))
    # print(link.find('span'))
    # print(link.find('a'))
    onMouseOver = link.find('a').get('onmouseover')
    if onMouseOver:
        startIdx = onMouseOver.find('"id":') + 5
        endIdx = onMouseOver.find(',', startIdx)
        gameId = onMouseOver[startIdx:endIdx]
    else:
        continue

    currentPlayers = link.find('span')
    todayPlayers = int(currentPlayers.find_next('span').get_text().replace(',', ''))
    currentPlayers = int(currentPlayers.get_text().replace(',', ''))
    
    topCurrentGameIds.append((currentPlayers, gameId))
    topTodayGameIds.append((todayPlayers, gameId))

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

topCurrentGameDetails = []
topCurrentrequestErrorGameIds = []
cnt = 0
for currentPlayers, gameId in topCurrentGameIds:
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
        topCurrentrequestErrorGameIds.append(gameId)
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
    topCurrentGameDetails.append(data)

    parsingEndTime = time.time()
    print(f'{cnt}번째 게임 parsing 완료, {parsingEndTime - requestEndTime:.2f}초 소요')
    print(f'{cnt}번째 게임 확보 완료, {parsingEndTime - requestStartTime:.2f}초 소요')

endTime = time.time()

print(f'{endTime - startTime:.2f}초 소요')
print(f'{len(topCurrentGameDetails)}개의 게임 detail 확보')

with open(r"topCurrentPlayerGames/topCurrentPlayerGames.pkl", "wb") as f:
    pickle.dump(topCurrentGameDetails, f)

print(f'{len(topCurrentrequestErrorGameIds)}개의 게임 detail 확보 실패')
if topCurrentrequestErrorGameIds:
    with open(r"topCurrentPlayerGames/topCurrentPlayerGamesFailed.pkl", "wb") as f:
        pickle.dump(topCurrentrequestErrorGameIds, f)

# topToday

topTodayGameIds.sort()
topTodayGameDetails = []
topTodayrequestErrorGameIds = []
for todayPlayers, gameId in topTodayGameIds:
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
        topTodayrequestErrorGameIds.append(gameId)
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
    topTodayGameDetails.append(data)

    parsingEndTime = time.time()
    print(f'{cnt}번째 게임 parsing 완료, {parsingEndTime - requestEndTime:.2f}초 소요')
    print(f'{cnt}번째 게임 확보 완료, {parsingEndTime - requestStartTime:.2f}초 소요')

endTime = time.time()

print(f'{endTime - startTime:.2f}초 소요')
print(f'{len(topTodayGameDetails)}개의 게임 detail 확보')

with open(r"topCurrentPlayerGames/topTodayPlayerGames.pkl", "wb") as f:
    pickle.dump(topTodayGameDetails, f)

print(f'{len(topTodayrequestErrorGameIds)}개의 게임 detail 확보 실패')
if topTodayrequestErrorGameIds:
    with open(r"topCurrentPlayerGames/topTodayGamesFailed.pkl", "wb") as f:
        pickle.dump(topTodayrequestErrorGameIds, f)