from rest_framework.routers import DefaultRouter
from api import views
from . import dataControl
from . import dataProcess
from django.urls import path

router = DefaultRouter(trailing_slash=False)
router.register(r"app", views.AppViewSet)
router.register(r"surveyResult", views.SurveyResusltViewSet)
router.register(r"surveyQuestion", views.SurveyQuestionViewSet)
router.register(r"recommendationSurvey", views.recommendationSurveyViewSet)
router.register(r"game", views.GameViewSet)
router.register(r"newGame", views.NewGameViewSet)
router.register(r"popularGame", views.PopularGameViewSet)
router.register(r"topCurrentPlayerGame", views.TopCurrentPlayerGameViewSet)
router.register(r"topTodayPlayerGame", views.TopTodayPlayerGameViewSet)
router.register(r"favorite", views.FavoriteViewSet)

functionPatterns = [
    path('userSteamData/', dataControl.userSteamData),
    path('survey/<str:user_id>', dataProcess.surveyRecommendation),
    path('gameLists/', dataControl.gameLists),
]

urlpatterns = router.urls + functionPatterns + [

    # favorite 게임 목록 뿌리는 함수
    path("favorite/game/<str:appid>", views.getGameListByAppid.as_view()),
    # search 함수
    path("search/game/<str:gameName>", views.searchByName.as_view()),
    path("recommendationSurvey/game/<str:appid>", views.recommendGameListByAppId.as_view()),
    # 여기부터 각 장르별로 찾는 함수 : RPG, 액션, 캐주얼, 어드벤처 ,인디, 전략, 레이싱, 무료, 싱글, 멀티
    path("find/game/RPG/<int:index>", views.FindByRPG.as_view()),
    path("find/game/ACT/<int:index>", views.FindByACT.as_view()),
    path("find/game/CAS/<int:index>", views.FindByCAS.as_view()),
    path("find/game/ADV/<int:index>", views.FindByADV.as_view()),
    path("find/game/IND/<int:index>", views.FindByIND.as_view()),
    path("find/game/STR/<int:index>", views.FindBySTR.as_view()),
    path("find/game/RAC/<int:index>", views.FindByRAC.as_view()),
    path("find/game/FRE/<int:index>", views.FindByFRE.as_view()),
    path("find/game/SPO/<int:index>", views.FindBySPO.as_view()),
    path("find/game/SIG/<int:index>", views.FindBySIG.as_view()),
    path("find/game/MUL/<int:index>", views.FindByMUL.as_view()),
    path("find/game/<userId>", views.GetGameById.as_view()),
]
