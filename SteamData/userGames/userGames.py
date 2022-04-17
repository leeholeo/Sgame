# '''
# Steam의 유저 데이터 수집
# web API
# Selenium을 통한 auto scrolling 이후 Beautifulsoup를 통한 html parsing
# '''
# import time
# import requests
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.by import By
# # from selenium.common.exceptions import NoSuchElementException
# # from selenium.common.exceptions import JavascriptException
# # from selenium.common.exceptions import TimeoutException
# # from bs4 import BeautifulSoup
# import pickle
# import env


# # constants
# STEAM_WEB_API_KEY = env.STEAM_WEB_API_KEY
# USER_GAMES_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
# LEAST_OWN_GAMES = 10
# ERROR_SLEEP_TIME = 10

# # time estimate
# startTime = time.time()

# # 1. DB에서 게임 id들 가져오기(임시로 pkl file)
# with open(r'gameReviews/userIdsFromGameReviews.pkl', 'rb') as f:
#     # uesrIds는 set 자료형이다.
#     userIds = pickle.load(f)

# print(f'{len(userIds)}개의 id를 바탕으로 steam web API 실행')

# with open(r'topSellers/topSellers.pkl', 'rb') as f:
#     # uesrIds는 set 자료형이다.
#     gameIds = pickle.load(f)
#     gameIds = set(gameIds)
    
# startUserIdsLen = len(userIds)
# startGameIdsLen = len(gameIds)
# # {userId(str): userGames(dict)}
# allUserGames = {}
# allUserGamesPlayTimePublic = {}
# errorCnt = 0
# privateCnt = 0
# smallGamesCnt = 0
# # cnt = 10
# for userId in userIds:
#     # cnt += 1
#     # if cnt > 50:
#     #     break
#     requestStartTime = time.time()
#     payload = {'format': 'json', 'key': STEAM_WEB_API_KEY, 'steamid': userId}
#     try:
#         response = requests.get(USER_GAMES_BASE_URL, params=payload).json()['response']
#     except Exception as e:
#         print(f'Error occurred! Error: {e}')
#         print(f'Pass steamId - {userId}')
#         time.sleep(ERROR_SLEEP_TIME)
#         errorCnt += 1
#         continue
    
#     # 비공개 상태이거나, 보유 게임 수가 너무 적은 경우 무시
#     if response == {}:
#         privateCnt += 1
#         continue
#     elif response['game_count'] < LEAST_OWN_GAMES:
#         smallGamesCnt += 1
#         continue
    
#     # {appId(int): playTime(int)}
#     userGameIds = []
#     userGames = {}
#     playTimePublic = False
#     for game in response['games']:
#         gameId = game['appid']
#         userGameIds.append(game['appid'])
#         gameIds.add(gameId)
#         playTime = game['playtime_forever']
#         if playTime != 0:
#             playTimePublic = True
#         userGames[gameId] = playTime
    
#     allUserGames[userId] = userGameIds
#     if playTimePublic:
#         allUserGamesPlayTimePublic[userId] = userGames

#     requestEndTime = time.time()
#     print(f'{userId} user의 userGames 데이터 수집 완료, {requestEndTime - requestStartTime:.2f} 초 소요')

# print(f'{errorCnt} 번의 에러 발생!!!')

# print(f'{len(allUserGames)} 명의 userGames 데이터 확보')
# print(f'그 중 {len(allUserGamesPlayTimePublic)} 명의 public playtime userGames 데이터 확보')
# print(f'{startUserIdsLen - len(allUserGames)} 명의 user 손실')
# print(f'{privateCnt} 명의 비공개 user')
# print(f'{smallGamesCnt} 명의 {LEAST_OWN_GAMES} 개보다 적은 게임 보유 user')

# with open(r'userGames/userGames.pkl', 'wb') as f:
#     pickle.dump(allUserGames, f)

# with open(r'userGames/userGamesPlayTimePublic.pkl', 'wb') as f:
#     pickle.dump(allUserGamesPlayTimePublic, f)

# print(f'{len(gameIds)} 개의 gameId 확보')
# print(f'{len(gameIds) - startGameIdsLen} 개의 gameId 추가')
# with open(r'userGames/allGameIds.pkl', 'wb') as f:
#     pickle.dump(gameIds, f)

# endTime = time.time()

# print(f'총 {endTime - startTime:.2f} 초 소요')


'''
Steam의 유저 데이터 수집
web API
Selenium을 통한 auto scrolling 이후 Beautifulsoup를 통한 html parsing
'''
from re import L
import time
import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import JavascriptException
# from selenium.common.exceptions import TimeoutException
# from bs4 import BeautifulSoup
import pickle
import env


# constants
STEAM_WEB_API_KEY = env.STEAM_WEB_API_KEY
USER_GAMES_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
LEAST_OWN_GAMES = 10
ERROR_SLEEP_TIME = 60

# time estimate
startTime = time.time()

# 1. DB에서 게임 id들 가져오기(임시로 pkl file)
with open('gameReviews/userIdsFromGameReviews.pkl', 'rb') as f:
    # uesrIds는 set 자료형이다.
    userIds = pickle.load(f)

# print(userIds)
# print(len(userIds))

userIds = sorted(list(userIds))
print(f'{len(userIds)}개의 id를 바탕으로 steam web API 실행')
    
startUserIdsLen = len(userIds)
# {userId(str): userGames(dict)}
allUserGames = {}
allUserGamesPlayTimePublic = {}
errorCnt = 0
privateCnt = 0
smallGamesCnt = 0
cnt = 0
for unit in range(100):
    startUserId = (startUserIdsLen // 100) * unit
    endUserId = (startUserIdsLen // 100) * unit
    if unit == 99:
        endUserId = startUserIdsLen

    for userId in userIds:
        cnt += 1
        if cnt % 100 == 0:
            time.sleep(11)
        
        if cnt % 250 == 0:
            print(f'{cnt} 번째 유저 요청')

        requestStartTime = time.time()
        payload = {'format': 'json', 'key': STEAM_WEB_API_KEY, 'steamid': userId}
        try:
            response = requests.get(USER_GAMES_BASE_URL, params=payload).json()['response']
        except Exception as e:
            print(f'Error occurred! Error: {e}')
            print(f'Pass steamId - {userId}')
            time.sleep(ERROR_SLEEP_TIME)
            errorCnt += 1
            continue
        
        # 비공개 상태이거나, 보유 게임 수가 너무 적은 경우 무시
        if not response:
            print('private setting')
            privateCnt += 1
            continue
        elif response['game_count'] < LEAST_OWN_GAMES:
            print('too small games')
            smallGamesCnt += 1
            continue
        
        # {appId(int): playTime(int)}
        userGameIds = []
        userGames = {}
        playTimePublic = False
        for game in response['games']:
            gameId = game['appid']
            userGameIds.append(gameId)
            playTime = game['playtime_forever']
            if playTime != 0:
                playTimePublic = True
            userGames[gameId] = playTime
        
        allUserGames[userId] = userGameIds
        if playTimePublic:
            allUserGamesPlayTimePublic[userId] = userGames

        requestEndTime = time.time()
        print(f'{userId} user의 userGames 데이터 수집 완료, {requestEndTime - requestStartTime:.2f} 초 소요')


    print(f'{len(allUserGames)} 명의 userGames 데이터 확보')
    print(f'그 중 {len(allUserGamesPlayTimePublic)} 명의 public playtime userGames 데이터 확보')
    print(f'{startUserIdsLen - len(allUserGames)} 명의 user 손실')
    print(f'{errorCnt} 번의 에러 발생!!!')
    print(f'{privateCnt} 명의 비공개 user')
    print(f'{smallGamesCnt} 명의 {LEAST_OWN_GAMES} 개보다 적은 게임 보유 user')

    with open(f'userGames/userGames{unit}.pkl', 'wb') as f:
        pickle.dump(allUserGames, f)

    with open(f'userGames/userGamesPlayTimePublic{unit}.pkl', 'wb') as f:
        pickle.dump(allUserGamesPlayTimePublic, f)

endTime = time.time()

print(f'총 {endTime - startTime:.2f} 초 소요')
