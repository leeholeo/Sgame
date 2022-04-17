'''
Steam의 리뷰 데이터 수집
Selenium을 통한 auto scrolling 이후 Beautifulsoup를 통한 html parsing
데이터에 끝이 존재(반복을 통한 전체 수집 불가능)
'''
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pickle
import env


# constants
PAGEDOWN_ITER_NUM = 1
PAGEDOWN_CYCLE_ITER_NUM = 1
PAGEDOWN_PAUSE_TIME = 0.1
STEAM_WEB_API_KEY = env.STEAM_WEB_API_KEY
GAME_REVIEWS_BASE_URL = 'https://steamcommunity.com/app/'
USER_RESOLVE_VANITY_BASE_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'

# time estimate
startTime = time.time()

# 1. DB에서 게임 id들 가져오기(임시로 pkl file)
with open(r'topSellers/topSellersIds.pkl', 'rb') as f:
    gameIds = pickle.load(f)

print(gameIds)
print(len(gameIds))
# 2. 게임 id들마다 review 데이터 크롤링
allUserIds = set()

service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(service=service, options=options)
for order, gameId in enumerate(gameIds):
    crawlingStartTime = time.time()

    url = GAME_REVIEWS_BASE_URL + gameId + '/reviews?l=korean'
    try:
        driver.get(url)
    except TimeoutException:
        continue

    # 연령 체크
    try:
        age_check = driver.find_element(by=By.ID, value='age_gate_btn_continue')
        age_check.click()
        # age_check.send_keys(Keys.ENTER)
    except NoSuchElementException:
        pass

    # page scrolling
    for _ in range(PAGEDOWN_CYCLE_ITER_NUM):
        for __ in range(PAGEDOWN_ITER_NUM):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(PAGEDOWN_PAUSE_TIME)
        
        # '더 보기' 처리
        try:
            driver.execute_script('CheckForMoreContent()')
        except JavascriptException:
            print(f'{order + 1}번째 scrolling에서 javascript exception 발생!!!')
            break

    scrollingEndTime = time.time()
    print(f'{order + 1}번째 scrolling에 {scrollingEndTime - crawlingStartTime:.2f}초 소요')

    # 3. review 데이터에서 user id들 추출
    # html parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    userIds = []
    # loop for all a tags
    iterCnt = 0
    for link in soup.find_all('a'):
        if iterCnt != 0:
            # a tag linked to user profile repeated fourth, ignore it
            iterCnt -= 1
            continue

        # get value of attribute "href"
        userId = link.get('href')
        if type(userId) != type('str'):
            continue
        # two types of user profile urls
        if userId[:36] == 'https://steamcommunity.com/profiles/':
            iterCnt = 3
            userId = userId[36:-1]
            userIds.append(userId)
        elif userId[:30] == 'https://steamcommunity.com/id/':
            # 10,000,000 개 수집에 약 400시간.. 시간을 단축할 필요가 있다.
            # 비동기 사용?
            iterCnt = 3
            payload = {'key': STEAM_WEB_API_KEY, 'vanityurl': userId[30:-1]}
            try:
                # response = json.loads(requests.get(USER_RESOLVE_VANITY_BASE_URL, params=payload).text)
                response = requests.get(USER_RESOLVE_VANITY_BASE_URL, params=payload).json()
            except Exception as e:
                print(f'!!!Error occured, {e}\nsleep 60s')
                time.sleep(60)
                continue
            userId = response['response'].get('steamid', None)
            if userId is None:
                continue
            userIds.append(userId)
        
    # print(userIds)
    crawlingEndTime = time.time()
    print(f'{order + 1}번째 html parsing에 {crawlingEndTime - scrollingEndTime:.2f}초 소요')
    print(f'{len(userIds)} 개의 id 수집')
    # 중복 제거 필요 -> gameIds 혹은 db 저장 시 제거
    # 4. 추출한 user id들을 DB에 저장(임시로 pkl file)

    allUserIds.update(userIds)
    updateEndTime = time.time()
    print(f'{order + 1}번째 update에 {updateEndTime - crawlingEndTime:.2f}초 소요')
    print(f'{order + 1}번째 cycle에 {updateEndTime - crawlingStartTime:.2f}초 소요')

dumpingStartTime = time.time()
print(f'user id 추출에 {dumpingStartTime - startTime:.2f}초 소요')
print(f'{len(allUserIds)} 개의 id 수집')

# 데이터 검증 및 수정
toDeletes = []
for userId in allUserIds:
    userIdLen = len(userId)
    if userIdLen != 17:
        toDeletes.append(userId)

for toDelte in toDeletes:
    toDelteLen = len(toDelte)
    if toDelteLen > 17:
        allUserIds.add(toDelte[:17])
        allUserIds.remove(toDelte)
    else:
        allUserIds.remove(toDelte)

with open('userIdsFromGameReviews.pkl', 'wb') as f:
    pickle.dump(allUserIds, f)

endTime = time.time()
print(f'데이터 저장에 {endTime - dumpingStartTime:.2f}초 소요')
