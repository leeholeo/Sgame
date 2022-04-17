# from .models import Store
from .models import NewGame, PopularGame, TopCurrentPlayerGame, TopTodayPlayerGame, app
from .models import surveyResult
from .models import surveyQuestion
from .models import recommendationSurvey
from .models import game
from .models import favorite
from rest_framework import serializers


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = app
        fields = [
            "appId",
        ]

class GameSerializer(serializers.ModelSerializer):
    pc_requirements = serializers.JSONField(allow_null=True)
    developers = serializers.JSONField(allow_null=True)
    publishers = serializers.JSONField()
    price_overview = serializers.JSONField(allow_null=True)
    metacritic = serializers.JSONField(allow_null=True)
    categories = serializers.JSONField(allow_null=True)
    genres = serializers.JSONField()
    screenshots = serializers.JSONField()
    movies = serializers.JSONField(allow_null=True)

    class Meta:
        model = game
        fields = [
            "name",
            "steam_appid",
            "required_age",
            "detailed_description",
            "about_the_game",
            "short_description",
            "header_image",
            "website",
            "pc_requirements",
            "legal_notice",
            "publishers",
            "developers",
            "price_overview",
            "metacritic",
            "reviewRating",
            "ratingPercent",
            "reviewCount",
            "categories",
            "genres",
            "screenshots",
            "movies",
            "release_date",
            "background",
            "background_raw",
        ]

class GameRatingSerializer(GameSerializer):

    class Meta:
        model = game
        exclude = [
            "reviewRating",
            "ratingPercent",
            "reviewCount",
        ]

class NewGameSerializer(GameSerializer):

    class Meta:
        model = NewGame
        fields = '__all__'

class PopularGameSerializer(GameSerializer):

    class Meta:
        model = PopularGame
        fields = '__all__'

class TopCurrentPlayerGameSerializer(GameSerializer):

    class Meta:
        model = TopCurrentPlayerGame
        fields = '__all__'

class TopTodayPlayerGameSerializer(GameSerializer):

    class Meta:
        model = TopTodayPlayerGame
        fields = '__all__'

class NewGameRatingSerializer(GameSerializer):

    class Meta:
        model = NewGame
        exclude = [
            "reviewRating",
            "ratingPercent",
            "reviewCount",
        ]

class PopularGameRatingSerializer(GameSerializer):

    class Meta:
        model = PopularGame
        exclude = [
            "reviewRating",
            "ratingPercent",
            "reviewCount",
        ]

class TopCurrentGameRatingSerializer(GameSerializer):

    class Meta:
        model = TopCurrentPlayerGame
        exclude = [
            "reviewRating",
            "ratingPercent",
            "reviewCount",
        ]

class TopTodayGameRatingSerializer(GameSerializer):

    class Meta:
        model = TopTodayPlayerGame
        exclude = [
            "reviewRating",
            "ratingPercent",
            "reviewCount",
        ]

class SurveyResultSerializer(serializers.ModelSerializer):
    result = serializers.JSONField()

    class Meta:
        model = surveyResult
        fields = [
            "appId",
            'result',
        ]

class SurveyQuestionSerializer(serializers.ModelSerializer):
    question = serializers.JSONField()

    class Meta:
        model = surveyQuestion
        fields = [
            "id",
            "question",
        ]

class RecommendationsSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = recommendationSurvey
        fields = '__all__'


class favoriteSerializer(serializers.ModelSerializer):
    gameList = serializers.JSONField()

    class Meta:
        model = favorite
        fields = [
            "appId",
            "gameList",
        ]
