'''
Steam의 신작 데이터 수집
bs4를 이용한 크롤링
'''
import time
import requests
from bs4 import BeautifulSoup
import pickle


# constants
GAMES_BASE_URL = 'https://store.steampowered.com/app/'

# time estimate
startTime = time.time()


# 2. 게임 id 크롤링, bs4여도 상관이 없다
with open(r'userGames/allGameIds.pkl', 'rb') as f:
    allGameIds = pickle.load(f)

print()
gameRatings = {}
cnt = 0
payload = { 'l': 'korean' }
allGameIdsIntList = list(map(int, allGameIds))
allGameIdsIntList.sort()
allGameIds = list(map(str, allGameIdsIntList))
allGameIdsNum = len(allGameIds)
for unit in range(7, 10):
    startGameId = (allGameIdsNum // 10) * unit 
    endGameId = (allGameIdsNum // 10) * (unit + 1)
    if unit == 9:
        endGameId = allGameIdsNum
    for gameId in allGameIds[startGameId:endGameId]:
        if cnt % 100 == 0:
            print(f'{cnt} 번째 rating 추출')
        
        cnt += 1
        # print(f'ㅡㅡㅡㅡㅡㅡㅡㅡ{gameId}ㅡㅡㅡㅡㅡㅡㅡㅡ')
        try:
            response = requests.get(GAMES_BASE_URL + str(gameId), params=payload).text
        except Exception as e:
            print(f'Error occurred! Error: {e}')
            print(gameId)
            time.sleep(60)
            continue
        soup = BeautifulSoup(response, 'html.parser')

        reviewRating = ''
        reviewCount = -1
        ratingPercent = -1
        for link in soup.find_all('div', attrs={ 'class': 'user_reviews_summary_row' }):
            subtitle = link.find('div', attrs={ 'class': 'subtitle' }).get_text()
            if subtitle != '모든 평가':
                continue
            
            spans = link.find('div', attrs={ 'class': 'summary' }).find_all('span')
            if len(spans) < 2:
                continue

            if spans[1].get('class') != ['responsive_reviewdesc_short']:
                continue
            
            reviewRating = spans[0].get_text()
            reviewRaw = spans[1].get_text().strip()
            reviewCount = reviewRaw[reviewRaw.find('/') + 1:reviewRaw.find(')')].replace(',', '')
            ratingPercent = reviewRaw[1:reviewRaw.find('%')].replace(',', '')

            if reviewCount.isdigit() and ratingPercent.isdigit():
                gameRatings[gameId] = {
                    'reviewRaw' : reviewRating,
                    'reviewCount' : int(reviewCount),
                    'ratingPercent' : int(ratingPercent)
                }
            else:
                pass

            # print(gameRatings.get(gameId))

    endTime = time.time()

    print(f'{endTime - startTime:.2f}초 소요')
    print(f'{len(gameRatings)}개의 게임 rating 확보')

    with open(f"gameRatings/gameRatings{unit}.pkl", "wb") as f:
        pickle.dump(gameRatings, f)

    print(f'{ len(allGameIds) - len(gameRatings)}개의 게임 rating 확보 실패')
