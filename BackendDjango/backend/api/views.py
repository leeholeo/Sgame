from api import models, serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import random
import re
import requests

API_KEY = "F0B488C9E39737CF0BD0270321060EB8"

ACT_list = []
ADV_list = []
CAS_list = []
FRE_list = []
IND_list = []
MUL_list = []
RAC_list = []
RPG_list = []
SIG_list = []
SPO_list = []
STR_list = []

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class AppViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AppSerializer
    queryset = models.app.objects.all()

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GameSerializer
    queryset = models.game.objects.all()

class SurveyResusltViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SurveyResultSerializer
    queryset = models.surveyResult.objects.all()

class SurveyQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SurveyQuestionSerializer
    queryset = models.surveyQuestion.objects.all()

class recommendationSurveyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecommendationsSurveySerializer
    queryset = models.recommendationSurvey.objects.all()

class NewGameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NewGameSerializer
    queryset = models.NewGame.objects.all()

class PopularGameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PopularGameSerializer
    queryset = models.PopularGame.objects.all()

class TopCurrentPlayerGameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TopCurrentPlayerGameSerializer
    queryset = models.TopCurrentPlayerGame.objects.all()

class TopTodayPlayerGameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TopTodayPlayerGameSerializer
    queryset = models.TopTodayPlayerGame.objects.all()

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.favoriteSerializer
    queryset = models.favorite.objects.all()

# 즐겨찾기
class getGameListByAppid(APIView):
    def get(self, request, appid):
        user = models.favorite.objects.filter(appId=appid)
        user_serializer = serializers.favoriteSerializer(user, many=True)
        favorite_num_list = user_serializer.data[0]["gameList"]

        game_list = []

        for game in favorite_num_list:
            game_serializer = serializers.GameSerializer(models.game.objects.filter(steam_appid=game["steam_appid"]), many=True)
            if game_serializer.data:
                game_list.append(game_serializer.data[0])

        return Response(game_list)

# 검색기능
class searchByName(APIView):
    def get(self, request, gameName):
        gameName = re.sub(r"[^a-zA-Z0-9]","",gameName)
        game_all = models.game.objects.all()
        game_list = serializers.GameSerializer(game_all, many=True)

        ans = []
        for game in game_list.data:
            name = re.sub(r"[^a-zA-Z0-9]","",game['name'])
            if gameName.lower() in name.lower():
                ans.append(game)
        return Response(ans)


# 여기부터 장르별로 find 하는거

class FindByRPG(APIView):
    def get(self, request, index):
        if not RPG_list:
            genFiltered = models.game.objects.filter(genres={'description': 'RPG'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                RPG_list.append(game)
        
        length = len(RPG_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(RPG_list[i])
        else:
            for i in range(length):
                ans.append(RPG_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByACT(APIView):
    def get(self, request, index):
        if not ACT_list:
            genFiltered = models.game.objects.filter(genres={'description': '액션'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                ACT_list.append(game)
        
        length = len(ACT_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(ACT_list[i])
        else:
            for i in range(length):
                ans.append(ACT_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByCAS(APIView):
    def get(self, request, index):
        if not CAS_list:
            genFiltered = models.game.objects.filter(genres={'description': '캐주얼'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                CAS_list.append(game)
        
        length = len(CAS_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(CAS_list[i])
        else:
            for i in range(length):
                ans.append(CAS_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByADV(APIView):
    def get(self, request, index):
        if not ADV_list:
            genFiltered = models.game.objects.filter(genres={'description': '어드벤처'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                ADV_list.append(game)
        
        length = len(ADV_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(ADV_list[i])
        else:
            for i in range(length):
                ans.append(ADV_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByIND(APIView):
    def get(self, request, index):
        if not IND_list:
            genFiltered = models.game.objects.filter(genres={'description': '인디'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                IND_list.append(game)
        
        length = len(IND_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(IND_list[i])
        else:
            for i in range(length):
                ans.append(IND_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindBySTR(APIView):
    def get(self, request, index):
        if not STR_list:
            genFiltered = models.game.objects.filter(genres={'description': '전략'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                STR_list.append(game)
        
        length = len(STR_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(STR_list[i])
        else:
            for i in range(length):
                ans.append(STR_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByRAC(APIView):
    def get(self, request, index):
        if not RAC_list:
            genFiltered = models.game.objects.filter(genres={'description': '레이싱'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                RAC_list.append(game)
        
        length = len(RAC_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(RAC_list[i])
        else:
            for i in range(length):
                ans.append(RAC_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByFRE(APIView):
    def get(self, request, index):
        if not FRE_list:
            genFiltered = models.game.objects.filter(genres={'description': '무료'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                FRE_list.append(game)
        
        length = len(FRE_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(FRE_list[i])
        else:
            for i in range(length):
                ans.append(FRE_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindBySPO(APIView):
    def get(self, request, index):
        if not SPO_list:
            genFiltered = models.game.objects.filter(genres={'description': '스포츠'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                SPO_list.append(game)
        
        length = len(SPO_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(SPO_list[i])
        else:
            for i in range(length):
                ans.append(SPO_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindBySIG(APIView):
    def get(self, request, index):
        if not SIG_list:
            genFiltered = models.game.objects.filter(categories={'description': '싱글 플레이어'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                SIG_list.append(game)
        
        length = len(SIG_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(SIG_list[i])
        else:
            for i in range(length):
                ans.append(SIG_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class FindByMUL(APIView):
    def get(self, request, index):
        if not MUL_list:
            genFiltered = models.game.objects.filter(categories={'description': '멀티플레이어'}, reviewCount__gte=2000, ratingPercent__gte=80,metacritic__gte={'score':0})
            for game in genFiltered:
                MUL_list.append(game)
        
        length = len(MUL_list)
        ans = []

        if length >= 30:
            randSample = random.sample(range(length), index)
            for i in randSample:
                ans.append(MUL_list[i])
        else:
            for i in range(length):
                ans.append(MUL_list[i])

        serializer = serializers.GameSerializer(ans, many=True)

        return Response(serializer.data)

class GetGameById(APIView):
    def get(self, request, userId):
        FIND_STEAMID_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
        payload = {'format' : 'json', 'key': API_KEY, 'vanityurl': userId}
        response = requests.get(FIND_STEAMID_URL, params=payload).json()['response']
        print(response)

        steamId = response["steamid"]
        USER_GAMES_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        payload = {'format': 'json', 'key': API_KEY, 'steamid': steamId}
        response = requests.get(USER_GAMES_BASE_URL, params=payload).json()['response']

        appids = []
        r_len = response["game_count"]

        for i in range(r_len):
            appids.append(response["games"][i]["appid"])

        print(appids)

        game_list = []

        for i in range(r_len):
            game_serializer = serializers.GameSerializer(models.game.objects.filter(steam_appid=appids[i]), many=True)
            game_list += game_serializer.data

        return Response(game_list)

class recommendGameListByAppId(APIView):
    def get(self, request, appid):
        user = models.recommendationSurvey.objects.filter(appId=appid)
        user_serializer = serializers.RecommendationsSurveySerializer(user, many=True)
        recommendation_num_list = user_serializer.data  
        game_list = []

        for i in range(20):
            R = 'R' + str(i + 1)
            if recommendation_num_list[0][R]:
                game_serializer = serializers.GameSerializer(models.game.objects.filter(steam_appid=recommendation_num_list[0][R]), many=True)
                game_list.append(game_serializer.data[0])
            else:
                break

        return Response(game_list)
