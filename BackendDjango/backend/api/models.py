from djongo import models
from django import forms


class app(models.Model):
    appId = models.CharField(max_length=100, blank=False, null=False, primary_key=True)

    class Meta:
        db_table = 'app'


class GamePlayTime(models.Model):
    gameId = models.IntegerField()
    playTime = models.IntegerField()

    class Meta:
        abstract = True


class GamePlayTimeForm(forms.ModelForm):
    class Meta:
        model = GamePlayTime
        fields = (
            'gameId', 'playTime',
        )


class UserSteamData(models.Model):
    steamId = models.IntegerField(primary_key=True)
    isPlayTimePublic = models.BooleanField()
    gamePlayTime = models.ArrayField(
        model_container=GamePlayTime,
        model_form_class=GamePlayTimeForm,
    )

    class Meta:
        db_table='UserSteamData'


class GameBase(models.Model):
    name = models.CharField(max_length=100)
    steam_appid = models.IntegerField(primary_key=True)
    required_age = models.IntegerField()
    detailed_description = models.TextField()
    about_the_game = models.TextField()
    short_description = models.TextField()
    header_image = models.CharField(max_length=100)
    website = models.CharField(max_length=100, blank=True, null=True)
    pc_requirements = models.JSONField(blank=True, null=True)
    legal_notice = models.TextField(blank=True, null=True)
    developers = models.JSONField(blank=True, null=True)
    publishers = models.JSONField()
    price_overview = models.JSONField(blank=True, null=True)
    metacritic = models.JSONField(blank=True, null=True)
    reviewRating = models.CharField(max_length=100, null=True)
    ratingPercent = models.IntegerField(null=True)
    reviewCount = models.IntegerField(null=True)
    categories = models.JSONField(blank=True, null=True)
    genres = models.JSONField()
    screenshots = models.JSONField(blank=True, null=True)
    movies = models.JSONField(blank=True, null=True)
    release_date = models.JSONField(blank=True, null=True)
    background = models.CharField(max_length=100)
    background_raw = models.CharField(max_length=100)

    class Meta:
        abstract = True


class game(GameBase):

    class Meta:
        db_table = 'game'


class NewGame(GameBase):
    
    class Meta:
        db_table = 'NewGame'


class PopularGame(GameBase):
    
    class Meta:
        db_table = 'PopularGame'


class TopCurrentPlayerGame(GameBase):
    
    class Meta:
        db_table = 'TopCurrentPlayerGame'


class TopTodayPlayerGame(GameBase):
    
    class Meta:
        db_table = 'TopTodayPlayerGame'


class surveyResult(models.Model):
    appId = models.OneToOneField("app", related_name="appId+", on_delete=models.CASCADE, db_column="appId",
                                 primary_key=True)
    result = models.JSONField(blank=False, null=False)

    class Meta:
        db_table = 'surveyResult'


class surveyQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.JSONField(blank=False, null=False)

    class Meta:
        db_table = 'surveyQuestion'


class recommendationSurvey(models.Model):
    appId = models.OneToOneField("app", related_name="appId+", on_delete=models.DO_NOTHING, db_column="appId", primary_key=True)
    R1 = models.ForeignKey("game", related_name="R1+", on_delete=models.CASCADE, db_column="R1", blank=True, null=True)
    R2 = models.ForeignKey("game", related_name="R2+", on_delete=models.CASCADE, db_column="R2", blank=True, null=True)
    R3 = models.ForeignKey("game", related_name="R3+", on_delete=models.CASCADE, db_column="R3", blank=True, null=True)
    R4 = models.ForeignKey("game", related_name="R4+", on_delete=models.CASCADE, db_column="R4", blank=True, null=True)
    R5 = models.ForeignKey("game", related_name="R5+", on_delete=models.CASCADE, db_column="R5", blank=True, null=True)
    R6 = models.ForeignKey("game", related_name="R6+", on_delete=models.CASCADE, db_column="R6", blank=True, null=True)
    R7 = models.ForeignKey("game", related_name="R7+", on_delete=models.CASCADE, db_column="R7", blank=True, null=True)
    R8 = models.ForeignKey("game", related_name="R8+", on_delete=models.CASCADE, db_column="R8", blank=True, null=True)
    R9 = models.ForeignKey("game", related_name="R9+", on_delete=models.CASCADE, db_column="R9", blank=True, null=True)
    R10 = models.ForeignKey("game", related_name="R10+", on_delete=models.CASCADE, db_column="R10", blank=True, null=True)
    R11 = models.ForeignKey("game", related_name="R11+", on_delete=models.CASCADE, db_column="R11", blank=True, null=True)
    R12 = models.ForeignKey("game", related_name="R12+", on_delete=models.CASCADE, db_column="R12", blank=True, null=True)
    R13 = models.ForeignKey("game", related_name="R13+", on_delete=models.CASCADE, db_column="R13", blank=True, null=True)
    R14 = models.ForeignKey("game", related_name="R14+", on_delete=models.CASCADE, db_column="R14", blank=True, null=True)
    R15 = models.ForeignKey("game", related_name="R15+", on_delete=models.CASCADE, db_column="R15", blank=True, null=True)
    R16 = models.ForeignKey("game", related_name="R16+", on_delete=models.CASCADE, db_column="R16", blank=True, null=True)
    R17 = models.ForeignKey("game", related_name="R17+", on_delete=models.CASCADE, db_column="R17", blank=True, null=True)
    R18 = models.ForeignKey("game", related_name="R18+", on_delete=models.CASCADE, db_column="R18", blank=True, null=True)
    R19 = models.ForeignKey("game", related_name="R19+", on_delete=models.CASCADE, db_column="R19", blank=True, null=True)
    R20 = models.ForeignKey("game", related_name="R20+", on_delete=models.CASCADE, db_column="R20", blank=True, null=True)

    class Meta:
        db_table = 'recommendationSurvey'

class favorite(models.Model):
    appId = models.OneToOneField("app", related_name="appId+", on_delete=models.DO_NOTHING, db_column="appId", primary_key=True)
    gameList = models.JSONField(null=True)

    class Meta:
        db_table = 'favorite'
