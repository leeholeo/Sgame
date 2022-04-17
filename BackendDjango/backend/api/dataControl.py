from .models import (
    NewGame, PopularGame, game as Game,
    NewGame, PopularGame, TopCurrentPlayerGame,
    TopTodayPlayerGame, surveyResult as SurveyResult,
    surveyQuestion as SurveyQuestion,
    recommendationSurvey as RecommendationSurvey,
    favorite as Favorite, app as App,

)
from .models import UserSteamData
from .serializers import (
    GameRatingSerializer, NewGameRatingSerializer,
    PopularGameRatingSerializer, SurveyQuestionSerializer,
    SurveyResultSerializer, TopCurrentGameRatingSerializer,
    TopTodayGameRatingSerializer, AppSerializer,
    RecommendationsSurveySerializer,
    favoriteSerializer as FavoriteSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import pickle
import requests
from bs4 import BeautifulSoup




GAMES_CRAWLING_BASE_URL = 'https://store.steampowered.com/app/'
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


# 게임 하나의 rating 크롤링
def getGameRating(gameId):
    payload = { 'l': 'korean' }

    try:
        response = requests.get(GAMES_CRAWLING_BASE_URL + gameId, params=payload).text
    except Exception as e:
        print(f'Error occurred! Error: {e}')
        return f'Error occurred! Error: {e}'

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
            return {
                'reviewRaw' : reviewRating,
                'reviewCount' : int(reviewCount),
                'ratingPercent' : int(ratingPercent)
            }
        else:
            pass
    
    return f'Rating data cannot found'


# DB에 게임 하나 집어넣기
def insertGame(gameId):
    payload = { 'appids': gameId, 'l': 'korean' }
    try:
        response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()
    except Exception as e:
        print(f'Error occurred! Error: {e}')
        return f'Error occurred! Error: {e}'
        
    if not response:
        return 'No response!'

    response = response[gameId]
    if response['success'] == False:
        # 한국어 지원이 안 되는 게임인 경우
        return 'Korean not supported'

    response = response.get('data')
    if response['type'] != 'game':
        return 'Not a game'

    data = {}
    for key in KEYS:
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
    
    return data


@api_view(['GET'])
def userSteamData(requests):
    with open('api/dumpData/userGamesPlayTimePublic.pkl', 'rb') as f:
        userGames = pickle.load(f)
    
    cnt = 1
    for user, games in userGames.items():
        userSteamData = UserSteamData()
        playTimes = []
        for gameId, playTime in games.items():
            playTimes.append({ 'gameId': gameId, 'playTime': playTime })

        userSteamData.steamId = int(user)
        userSteamData.isPlayTimePublic = True
        userSteamData.gamePlayTime = playTimes
        userSteamData.save()
        cnt += 1
        if not cnt % 100:
            print(f'{cnt} userSteamData loaded')

    return Response({'notice': 'userSteamData loading completed'})


@api_view(['GET'])
def gameLists(requests):
    with open('api/dumpData/gameRatings.pkl', 'rb') as f:
        gameRatings = pickle.load(f)

    reviewRaws = [
        '압도적으로 긍정적',
        '매우 긍정적',
        '대체로 긍정적',
        '복합적',
        '대체로 부정적',
        '매우 부정적',
        '압도적으로 부정적'
    ]
    print('dumping allGameDetails...')
    cnt = 1
    with open(f'api/dumpData/allGameDetails.pkl', 'rb') as f:
        games = pickle.load(f)

    # Counter Strike 문제
    games.pop('100', None)

    noRating = 0
    noReviewRaw = 0
    noReviewCount = 0
    noPercent = 0
    notValid = 0
    for gameId, gameDetail in games.items():
        gameRating = gameRatings.get(gameId)
        if not gameRating:
            noRating += 1
            continue
        elif gameRating.get('reviewRaw') not in reviewRaws:
            noReviewRaw += 1
            continue
        elif type(gameRating.get('reviewCount')) != int:
            noReviewCount += 1
            continue
        elif type(gameRating.get('ratingPercent')) != int:
            noPercent += 1
            continue

        gameSerializer = GameRatingSerializer(data=gameDetail)
        if gameSerializer.is_valid():
            game = gameSerializer.save()
            if not game.website:
                game.website = 'https://store.steampowered.com/app/' + gameId
            game.reviewRating = gameRating['reviewRaw']
            game.ratingPercent = gameRating['ratingPercent']
            game.reviewCount = gameRating['reviewCount']
            game.save()
        else:
            notValid += 1

        cnt += 1

    print('dumping newGames...')
    cnt = 1

    with open('api/dumpData/newGames.pkl', 'rb') as f:
        newGames = pickle.load(f)
    
    noRating = 0
    noReviewRaw = 0
    noReviewCount = 0
    noPercent = 0
    notValid = 0
    for gameId, gameDetail in newGames.items():
        if NewGame.objects.filter(steam_appid=gameId):
            continue

        gameRating = gameRatings.get(gameId)
        if not gameRating:
            gameRating = getGameRating(gameId)
            
        if type(gameRating) != dict:
            noRating += 1
            continue
        elif gameRating.get('reviewRaw') not in reviewRaws:
            noReviewRaw += 1
            continue
        elif type(gameRating.get('reviewCount')) != int:
            noReviewCount += 1
            continue
        elif type(gameRating.get('ratingPercent')) != int:
            noPercent += 1
            continue

        gameSerializer = NewGameRatingSerializer(data=gameDetail)
        if gameSerializer.is_valid():
            game = gameSerializer.save()
            if not game.website:
                game.website = 'https://store.steampowered.com/app/' + gameId
            game.reviewRating = gameRating['reviewRaw']
            game.ratingPercent = gameRating['ratingPercent']
            game.reviewCount = gameRating['reviewCount']
            game.save()
        else:
            notValid += 1

        cnt += 1

    print('dumping popularGames...')
    cnt = 1

    with open('api/dumpData/topSellers.pkl', 'rb') as f:
        popularGames = pickle.load(f)

    noRating = 0
    noReviewRaw = 0
    noReviewCount = 0
    noPercent = 0
    notValid = 0
    for gameDetail in popularGames:
        gameId = str(gameDetail.get('steam_appid'))
        if PopularGame.objects.filter(steam_appid=gameId):
            continue
        
        gameRating = gameRatings.get(gameId)
        if not gameRating:
            gameRating = getGameRating(gameId)

        if type(gameRating) != dict:
            noRating += 1
            continue
        elif gameRating.get('reviewRaw') not in reviewRaws:
            noReviewRaw += 1
            continue
        elif type(gameRating.get('reviewCount')) != int:
            noReviewCount += 1
            continue
        elif type(gameRating.get('ratingPercent')) != int:
            noPercent += 1
            continue

        gameSerializer = PopularGameRatingSerializer(data=gameDetail)
        if gameSerializer.is_valid():
            game = gameSerializer.save()
            if not game.website:
                game.website = 'https://store.steampowered.com/app/' + gameId
            game.reviewRating = gameRating['reviewRaw']
            game.ratingPercent = gameRating['ratingPercent']
            game.reviewCount = gameRating['reviewCount']
            game.save()
        else:
            notValid += 1

        cnt += 1
 
    print('dumping topCurrentPlayerGames...')
    cnt = 1

    with open('api/dumpData/topCurrentPlayerGames.pkl', 'rb') as f:
        topCurrentPlayerGames = pickle.load(f)

    noRating = 0
    noReviewRaw = 0
    noReviewCount = 0
    noPercent = 0
    notValid = 0
    for gameDetail in topCurrentPlayerGames.values():
        gameId = str(gameDetail.get('steam_appid'))
        gameRating = gameRatings.get(gameId)
        if not gameRating:
            noRating += 1
            continue
        elif gameRating.get('reviewRaw') not in reviewRaws:
            noReviewRaw += 1
            continue
        elif type(gameRating.get('reviewCount')) != int:
            noReviewCount += 1
            continue
        elif type(gameRating.get('ratingPercent')) != int:
            noPercent += 1
            continue

        gameSerializer = TopCurrentGameRatingSerializer(data=gameDetail)
        if gameSerializer.is_valid():
            game = gameSerializer.save()
            if not game.website:
                game.website = 'https://store.steampowered.com/app/' + gameId
            game.reviewRating = gameRating['reviewRaw']
            game.ratingPercent = gameRating['ratingPercent']
            game.reviewCount = gameRating['reviewCount']
            game.save()
        else:
            notValid += 1


        cnt += 1

    print('dumping topTodayPlayerGames...')
    cnt = 1

    with open('api/dumpData/topTodayPlayerGames.pkl', 'rb') as f:
        topTodayPlayerGames = pickle.load(f)

    for gameDetail in topTodayPlayerGames.values():
        gameId = str(gameDetail.get('steam_appid'))
        gameRating = gameRatings.get(gameId)
        if not gameRating:
            continue
        elif gameRating.get('reviewRaw') not in reviewRaws:
            continue
        elif type(gameRating.get('reviewCount')) != int:
            continue
        elif type(gameRating.get('ratingPercent')) != int:
            continue

        gameSerializer = TopTodayGameRatingSerializer(data=gameDetail)
        if gameSerializer.is_valid():
            game = gameSerializer.save()
            if not game.website:
                game.website = 'https://store.steampowered.com/app/' + gameId
            game.reviewRating = gameRating['reviewRaw']
            game.ratingPercent = gameRating['ratingPercent']
            game.reviewCount = gameRating['reviewCount']
            game.save()

        cnt += 1

    return Response({'notice': 'gameLists loading completed'})


def userSteamDataDumping():
    with open('api/dumpData/userGamesPlayTimePublic.pkl', 'rb') as f:
        userGames = pickle.load(f)
    
    cnt = 1
    if UserSteamData.objects.all().count() == 0:
        for user, games in userGames.items():
            userSteamData = UserSteamData()
            playTimes = []
            for gameId, playTime in games.items():
                playTimes.append({ 'gameId': gameId, 'playTime': playTime })

            userSteamData.steamId = int(user)
            userSteamData.isPlayTimePublic = True
            userSteamData.gamePlayTime = playTimes
            userSteamData.save()
            cnt += 1
            if not cnt % 100:
                print(f'{cnt} userSteamData loaded')

    return Response({'notice': 'userSteamData loading completed'})


def gameListsDumping():
    with open('api/dumpData/gameRatings.pkl', 'rb') as f:
        gameRatings = pickle.load(f)

    reviewRaws = [
        '압도적으로 긍정적',
        '매우 긍정적',
        '대체로 긍정적',
        '복합적',
        '대체로 부정적',
        '매우 부정적',
        '압도적으로 부정적'
    ]
    if Game.objects.all().count() == 0:
        print('dumping allGameDetails...')
        cnt = 1
        with open(f'api/dumpData/allGameDetails.pkl', 'rb') as f:
            games = pickle.load(f)

        # Counter Strike 문제
        games.pop('100', None)

        noRating = 0
        noReviewRaw = 0
        noReviewCount = 0
        noPercent = 0
        notValid = 0
        for gameId, gameDetail in games.items():
            gameRating = gameRatings.get(gameId)
            if not gameRating:
                noRating += 1
                continue
            elif gameRating.get('reviewRaw') not in reviewRaws:
                noReviewRaw += 1
                continue
            elif type(gameRating.get('reviewCount')) != int:
                noReviewCount += 1
                continue
            elif type(gameRating.get('ratingPercent')) != int:
                noPercent += 1
                continue

            gameSerializer = GameRatingSerializer(data=gameDetail)
            if gameSerializer.is_valid():
                game = gameSerializer.save()
                if not game.website:
                    game.website = 'https://store.steampowered.com/app/' + gameId
                game.reviewRating = gameRating['reviewRaw']
                game.ratingPercent = gameRating['ratingPercent']
                game.reviewCount = gameRating['reviewCount']
                game.save()
            else:
                notValid += 1

            cnt += 1

    if NewGame.objects.all().count() == 0:
        print('dumping newGames...')
        cnt = 1

        with open('api/dumpData/newGames.pkl', 'rb') as f:
            newGames = pickle.load(f)
        
        noRating = 0
        noReviewRaw = 0
        noReviewCount = 0
        noPercent = 0
        notValid = 0
        for gameId, gameDetail in newGames.items():
            if NewGame.objects.filter(steam_appid=gameId):
                continue

            gameRating = gameRatings.get(gameId)
            if not gameRating:
                gameRating = getGameRating(gameId)
                
            if type(gameRating) != dict:
                noRating += 1
                continue
            elif gameRating.get('reviewRaw') not in reviewRaws:
                noReviewRaw += 1
                continue
            elif type(gameRating.get('reviewCount')) != int:
                noReviewCount += 1
                continue
            elif type(gameRating.get('ratingPercent')) != int:
                noPercent += 1
                continue

            gameSerializer = NewGameRatingSerializer(data=gameDetail)
            if gameSerializer.is_valid():
                game = gameSerializer.save()
                if not game.website:
                    game.website = 'https://store.steampowered.com/app/' + gameId
                game.reviewRating = gameRating['reviewRaw']
                game.ratingPercent = gameRating['ratingPercent']
                game.reviewCount = gameRating['reviewCount']
                game.save()
            else:
                notValid += 1

            cnt += 1

    if PopularGame.objects.all().count() == 0:
        print('dumping popularGames...')
        cnt = 1

        with open('api/dumpData/topSellers.pkl', 'rb') as f:
            popularGames = pickle.load(f)

        noRating = 0
        noReviewRaw = 0
        noReviewCount = 0
        noPercent = 0
        notValid = 0
        for gameDetail in popularGames:
            gameId = str(gameDetail.get('steam_appid'))
            if PopularGame.objects.filter(steam_appid=gameId):
                continue
            
            gameRating = gameRatings.get(gameId)
            if not gameRating:
                gameRating = getGameRating(gameId)

            if type(gameRating) != dict:
                noRating += 1
                continue
            elif gameRating.get('reviewRaw') not in reviewRaws:
                noReviewRaw += 1
                continue
            elif type(gameRating.get('reviewCount')) != int:
                noReviewCount += 1
                continue
            elif type(gameRating.get('ratingPercent')) != int:
                noPercent += 1
                continue

            gameSerializer = PopularGameRatingSerializer(data=gameDetail)
            if gameSerializer.is_valid():
                game = gameSerializer.save()
                if not game.website:
                    game.website = 'https://store.steampowered.com/app/' + gameId
                game.reviewRating = gameRating['reviewRaw']
                game.ratingPercent = gameRating['ratingPercent']
                game.reviewCount = gameRating['reviewCount']
                game.save()
            else:
                notValid += 1

            cnt += 1
    
    if TopCurrentPlayerGame.objects.all().count() == 0:
        print('dumping topCurrentPlayerGames...')
        cnt = 1

        with open('api/dumpData/topCurrentPlayerGames.pkl', 'rb') as f:
            topCurrentPlayerGames = pickle.load(f)

        noRating = 0
        noReviewRaw = 0
        noReviewCount = 0
        noPercent = 0
        notValid = 0
        for gameDetail in topCurrentPlayerGames.values():
            gameId = str(gameDetail.get('steam_appid'))
            gameRating = gameRatings.get(gameId)
            if not gameRating:
                noRating += 1
                continue
            elif gameRating.get('reviewRaw') not in reviewRaws:
                noReviewRaw += 1
                continue
            elif type(gameRating.get('reviewCount')) != int:
                noReviewCount += 1
                continue
            elif type(gameRating.get('ratingPercent')) != int:
                noPercent += 1
                continue

            gameSerializer = TopCurrentGameRatingSerializer(data=gameDetail)
            if gameSerializer.is_valid():
                game = gameSerializer.save()
                if not game.website:
                    game.website = 'https://store.steampowered.com/app/' + gameId
                game.reviewRating = gameRating['reviewRaw']
                game.ratingPercent = gameRating['ratingPercent']
                game.reviewCount = gameRating['reviewCount']
                game.save()
            else:
                notValid += 1


            cnt += 1

    if TopTodayPlayerGame.objects.all().count() == 0:
        print('dumping topTodayPlayerGames...')
        cnt = 1

        with open('api/dumpData/topTodayPlayerGames.pkl', 'rb') as f:
            topTodayPlayerGames = pickle.load(f)

        for gameDetail in topTodayPlayerGames.values():
            gameId = str(gameDetail.get('steam_appid'))
            gameRating = gameRatings.get(gameId)
            if not gameRating:
                continue
            elif gameRating.get('reviewRaw') not in reviewRaws:
                continue
            elif type(gameRating.get('reviewCount')) != int:
                continue
            elif type(gameRating.get('ratingPercent')) != int:
                continue

            gameSerializer = TopTodayGameRatingSerializer(data=gameDetail)
            if gameSerializer.is_valid():
                game = gameSerializer.save()
                if not game.website:
                    game.website = 'https://store.steampowered.com/app/' + gameId
                game.reviewRating = gameRating['reviewRaw']
                game.ratingPercent = gameRating['ratingPercent']
                game.reviewCount = gameRating['reviewCount']
                game.save()

            cnt += 1

    return Response({'notice': 'gameLists loading completed'})


def userDataDumping():
    if App.objects.all().count() == 0:
        with open(f'api/dumpData/app.json', 'r') as f:
            app = json.load(f)
        
        appSerializer = AppSerializer(data=app, many=True)
        if appSerializer.is_valid():
            appSerializer.save()
    
    if Favorite.objects.all().count() == 0:
        with open(f'api/dumpData/favorite.json', 'r') as f:
            favorite = json.load(f)
        
        favoriteSerializer = FavoriteSerializer(data=favorite, many=True)
        if favoriteSerializer.is_valid():
            favoriteSerializer.save()
    
    if RecommendationSurvey.objects.all().count() == 0:
        with open(f'api/dumpData/recommendationSurvey.json', 'r') as f:
            recommendationSurvey = json.load(f)
        
        recommendationsSurveySerializer = RecommendationsSurveySerializer(data=recommendationSurvey, many=True)
        if recommendationsSurveySerializer.is_valid():
            recommendationsSurveySerializer.save()
    
    if SurveyQuestion.objects.all().count() == 0:
        with open(f'api/dumpData/surveyQuestion.json', 'r', encoding='utf-8') as f:
            surveyQuestion = json.load(f)
        
        surveyQuestionSerializer = SurveyQuestionSerializer(data=surveyQuestion, many=True)
        if surveyQuestionSerializer.is_valid():
            surveyQuestionSerializer.save()
    
    if SurveyResult.objects.all().count() == 0:
        with open(f'api/dumpData/surveyResult.json', 'r', encoding='utf-8') as f:
            surveyResult = json.load(f)
        
        surveyResultSerializer = SurveyResultSerializer(data=surveyResult, many=True)
        if surveyResultSerializer.is_valid():
            surveyResultSerializer.save()
    