'''
Steam의 인기 게임 수집
Selenium을 통한 auto scrolling 이후 Beautifulsoup를 통한 html parsing
데이터에 끝이 존재(반복을 통한 전체 수집 불가능)
'''
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle


# constants
PAGEDOWN_ITER_NUM = 10  # 1000의 1/3 수준으로 충분할 것으로 보임
PAGEDOWN_PAUSE_TIME = 0.1

# time estimate
startTime = time.time()

# target url
url = 'https://store.steampowered.com/search/?filter=topsellers'
service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
# options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# page scrolling
for _ in range(PAGEDOWN_ITER_NUM):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(PAGEDOWN_PAUSE_TIME)

scrollingEndTime = time.time()
print(f'Scrolling에 {scrollingEndTime - startTime:.2f}초 소요')

# html parsing
soup = BeautifulSoup(driver.page_source, 'html.parser')
gameIds = []
# loop for all a tags
for link in soup.find_all('a'):
    # get value of attribute "data-ds-appid"
    gameId = link.get('data-ds-appid')
    if gameId:
        # if a game has DLCs, game_id is like "game_id,DLC1_id,DLC2_id"
        gameId = gameId.split(',')[0]
        gameIds.append(gameId)

# 중복 제거 필요 -> gameIds 혹은 db 저장 시 제거
# dlc 제거 필요 -> appdetail 요청 시 type 확인 후 game이 아닌 경우 제거

crawlingEndTime = time.time()
print(f'Html parsing에 {crawlingEndTime - scrollingEndTime:.2f}초 소요')
print(f'Crawling에 {scrollingEndTime - startTime:.2f} + {crawlingEndTime - scrollingEndTime:.2f} = {crawlingEndTime - startTime:.2f}초 소요')

print(gameIds)
print(f'{len(gameIds)} 개의 id 수집')

with open('topSellersIds.pkl', 'wb') as f:
    pickle.dump(gameIds, f)

dumpingTime = time.time()
print(f'데이터 저장에 {dumpingTime - crawlingEndTime:.2f}초 소요')