from rest_framework.decorators import api_view
from rest_framework.response import Response
from api import models
from api import serializers
import numpy as np
import random
import time


@api_view(['GET'])
def surveyRecommendation(request, user_id):
    startTime = time.time()

    RECOMMENDATION_NUMBER = 20
        
    targetSurveyResult = models.surveyResult.objects.filter(appId=user_id)
    theOtherSurveyResult = models.surveyResult.objects.exclude(appId=user_id).exclude(result=[])

    theOtherCount = theOtherSurveyResult.count()
    R = [0] * theOtherCount

    idxR = 0
    for otherSurveyResultDict in theOtherSurveyResult:
        RLine = [0] * 10
        otherSurveyResult = otherSurveyResultDict.result
        for idxRLine in range(10):
            RLine[idxRLine] = otherSurveyResult[idxRLine]['ans']
        R[idxR] = RLine
        idxR += 1
    
    targetR = [0] * 10
    for idxRLine in range(10):
        targetR[idxRLine] = targetSurveyResult[0].result[idxRLine]['ans']
    
    K = 2
    targetR = np.array(targetR)
    R = np.array(R)
    surveySimilarity = R * targetR
    similarity = np.sum(surveySimilarity, axis=1)
    
    topK = similarity.argsort()[-K:]

    kUserFavorite = []
    for kIdx in range(K - 1, -1, -1):
        similarUserIdx = int(topK[kIdx])
        similarUserId = theOtherSurveyResult[similarUserIdx].appId
        kUserFavorite.append(models.favorite.objects.get(appId=similarUserId))
    
    kFavoriteGameId = []
    kFavoriteGameIdExist = {}
    favoriteGameCnt = 0
    for userFavorite in kUserFavorite:
        if favoriteGameCnt >= 20:
                break

        for favoriteGame in userFavorite.gameList:
            if favoriteGameCnt >= 20:
                break

            favoriteGameId = favoriteGame['steam_appid']
            if kFavoriteGameIdExist.get(favoriteGameId):
                continue
            
            favoriteGameCnt += 1
            kFavoriteGameIdExist[favoriteGameId] = True
            kFavoriteGameId.append(favoriteGameId)
    
    kFavorite = []
    for favoriteGameId in kFavoriteGameId:
        favoriteGameDetail = models.game.objects.get(steam_appid=favoriteGameId)
        gameSerializer = serializers.GameSerializer(favoriteGameDetail)
        kFavorite.append(gameSerializer.data)

    majorGame = models.game.objects.filter(reviewCount__gte=2000, ratingPercent__gte=80, metacritic__gte={ 'score': 0 })
    majorGameCount = majorGame.count()
    randomMajorGameIdx = random.sample(range(majorGameCount), (RECOMMENDATION_NUMBER - favoriteGameCnt))
    for majorGameIdx in randomMajorGameIdx:
        kFavoriteGameId.append(majorGame[majorGameIdx].steam_appid)
        gameSerializer = serializers.GameSerializer(majorGame[majorGameIdx])
        kFavorite.append(gameSerializer.data)

    recommendationSurvey = {}
    recommendationSurvey['appId'] = user_id
    for resultIdx, favoriteGameId in enumerate(kFavoriteGameId):
        recommendationSurvey[f'R{resultIdx + 1}'] = kFavoriteGameId[resultIdx]
    
    for resultIdx in range(favoriteGameCnt, RECOMMENDATION_NUMBER):
        recommendationSurvey[f'R{resultIdx + 1}'] = kFavoriteGameId[resultIdx]

    if models.recommendationSurvey.objects.filter(appId=user_id).exists():
        recommendation = models.recommendationSurvey.objects.get(appId=user_id)
        recommendationSerializer = serializers.RecommendationsSurveySerializer(recommendation, data=recommendationSurvey)
        if recommendationSerializer.is_valid():
            recommendationSerializer.save()
    else:
        recommendationSerializer = serializers.RecommendationsSurveySerializer(data=recommendationSurvey)
        if recommendationSerializer.is_valid():
            recommendationSerializer.save()

    endTime = time.time()
    print(f'게임 추천에 {endTime - startTime:.2f}초 소요')
    return Response(kFavorite)
