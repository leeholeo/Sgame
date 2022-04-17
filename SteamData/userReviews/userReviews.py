'''
Steam user의 리뷰 데이터 수집
Selenium을 통한 auto scrolling 이후 Beautifulsoup를 통한 html parsing
Pagination에 유의해가며 데이터 수집
'''
import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import pickle


# constants
USER_REVIEWS_BASE_URL = 'https://steamcommunity.com/profiles/'

# time estimate
startTime = time.time()

# 1. DB에서 유저 id들 가져오기(임시로 pkl file)
with open(r'userGames/userGamesPlayTimePublic.pkl', 'rb') as f:
    userGames = pickle.load(f)

with open(r'userGames/allGameIds.pkl', 'rb') as f:
    gameIds = pickle.load(f)
    gameIdsLen = len(gameIds)

# userGames = {'76561198373765079': 0, '76561198352176112': 0}
userCnt = len(userGames)
timeOutErrorCnt = 0
timeOutErrorPageCnt = 0
valueErrorCnt = 0
userPrivateCnt = 0
userNoRecommendationCnt = 0
errorGameCnt = 0
timeOutErrors = defaultdict(list)
# {userId(str): userRecommendation(dict)}
userRecommendations = {}

# 2. 유저 id들마다 review 데이터 크롤링
service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
# options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용, 에러 로그 발생
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(service=service, options=options)
# 유저 id를 순회
for userId in userGames.keys():
    crawlingStartTime = time.time()

    # page가 존재하는지 확인
    page = 1
    url = USER_REVIEWS_BASE_URL + userId + f'/recommended/?p={page}'
    try:
        driver.get(url)
    except TimeoutException:
        timeOutErrorCnt += 1
        continue

    # Pagination 체크
    try:
        pagingText = driver.find_element(by=By.CLASS_NAME, value='workshopBrowsePagingInfo').get_attribute('innerText')
    except NoSuchElementException:
        userPrivateCnt += 1
        continue
    
    frontIdx = pagingText.find('of') + 3
    rearIdx = pagingText.find(' ', frontIdx)
    reviewNumber = pagingText[frontIdx: rearIdx]
    # print(f'pagingText: {pagingText}')
    # print(f'reviewNumber: {reviewNumber}')
    try:
        reviewNumber = int(reviewNumber)
    except ValueError:
        valueErrorCnt += 1
        continue

    pageNum, remainder = divmod(reviewNumber, 10)
    if remainder != 0:
        pageNum += 1
    
    if pageNum == 0:
        userNoRecommendationCnt += 1
        continue
    
    # print(f'pageNum: {pageNum}')
    userRecommendation = {}
    while page <= pageNum:
        url = USER_REVIEWS_BASE_URL + userId + f'/recommended/?p={page}'
        page += 1
        if page != 2:
            try:
                driver.get(url)
            except TimeoutException or WebDriverException:
                timeOutErrors[userId].append(page - 1)
                continue
            
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for reviewBox in soup.find_all('div', 'review_box'):
            # gameId 추출
            gameAtag = reviewBox.find('a', 'game_capsule_ctn')
            gameLink = gameAtag.get('href')
            if gameLink[:31] == 'https://steamcommunity.com/app/':
                gameId = gameLink[31:]
                if not gameId[-1].isdigit():
                    try:
                        gameId = int(gameId[:-1])
                    except ValueError:
                        errorGameCnt += 1
                        continue
                    
                    gameId = str(gameId)
            
            # print(f'gameId: {gameId}')

            # 평가 추출
            recommendationAtag = reviewBox.find('div', 'title').find('a')
            recommendationText = recommendationAtag.get_text()
            # if recommendationText == 'Recommended':
            if recommendationText == 'Recommended':
                userRecommendation[gameId] = 1
            elif recommendationText == 'Not Recommended':
                userRecommendation[gameId] = 0
            
            gameIds.add(gameId)
            
    userRecommendations[userId] = userRecommendation

    crawlingEndTime = time.time()
    print(f'User {userId}, {len(userRecommendation.keys())} 개의 게임 리뷰 수집')
    print(f'{crawlingEndTime - crawlingStartTime:.2f} 초 소요')


print(f'Timeout 에러에 한해 재실행, {len(timeOutErrors)}개의 에러')
errorRetryStartTime = time.time()
for userId, pages in timeOutErrors.items():
    for page in pages:
        url = USER_REVIEWS_BASE_URL + userId + f'/recommended/?p={page}'
        try:
            driver.get(url)
        except TimeoutException or WebDriverException:
            timeOutErrorPageCnt += 1
            continue
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for reviewBox in soup.find_all('div', 'review_box'):
            # gameId 추출
            gameAtag = reviewBox.find('a', 'game_capsule_ctn')
            gameLink = gameAtag.get('href')
            if gameLink[:31] == 'https://steamcommunity.com/app/':
                gameId = gameLink[31:]
                if not gameId[-1].isdigit():
                    try:
                        gameId = int(gameId[:-1])
                    except ValueError:
                        errorGameCnt += 1
                        continue
                    
                    gameId = str(gameId)
            
            # print(f'gameId: {gameId}')

            # 평가 추출
            recommendationAtag = reviewBox.find('div', 'title').find('a')
            recommendationText = recommendationAtag.get_text()
            # if recommendationText == 'Recommended':
            if recommendationText == 'Recommended':
                userRecommendations[userId][gameId] = 1
            elif recommendationText == 'Not Recommended':
                userRecommendations[userId][gameId] = 0
            
            gameIds.add(gameId)

errorRetryEndTime = time.time()
print(f'{timeOutErrorPageCnt}개의 페이지 에러 재발생')
print(f'에러 페이지 재시도에 {errorRetryEndTime - errorRetryStartTime:.2f}초 소요')

with open(r'userReviews/userReviews.pkl', 'wb') as f:
    pickle.dump(userRecommendations, f)

print(f'{len(gameIds) - gameIdsLen}개의 게임 id 추가 확보')
with open(r'userGames/allGameIds.pkl', 'wb') as f:
    pickle.dump(gameIds, f)

# print(userRecommendations)

print(f'userCnt: {userCnt}')
print(f'timeOutErrorCnt: {timeOutErrorCnt}')
print(f'valueErrorCnt: {valueErrorCnt}')
print(f'userPrivateCnt: {userPrivateCnt}')
print(f'userNoRecommendationCnt: {userNoRecommendationCnt}')
print(f'errorGameCnt: {errorGameCnt}')

endTime = time.time()
print(f'총 {endTime - startTime:.2f}초 소요')
