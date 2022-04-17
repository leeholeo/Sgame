# Generated by Django 3.1.12 on 2022-04-08 13:39

import api.models
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app',
            fields=[
                ('appId', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'app',
            },
        ),
        migrations.CreateModel(
            name='game',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('steam_appid', models.IntegerField(primary_key=True, serialize=False)),
                ('required_age', models.IntegerField()),
                ('detailed_description', models.TextField()),
                ('about_the_game', models.TextField()),
                ('short_description', models.TextField()),
                ('header_image', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('pc_requirements', djongo.models.fields.JSONField(blank=True, null=True)),
                ('legal_notice', models.TextField(blank=True, null=True)),
                ('developers', djongo.models.fields.JSONField(blank=True, null=True)),
                ('publishers', djongo.models.fields.JSONField()),
                ('price_overview', djongo.models.fields.JSONField(blank=True, null=True)),
                ('metacritic', djongo.models.fields.JSONField(blank=True, null=True)),
                ('reviewRating', models.CharField(max_length=100, null=True)),
                ('ratingPercent', models.IntegerField(null=True)),
                ('reviewCount', models.IntegerField(null=True)),
                ('categories', djongo.models.fields.JSONField(blank=True, null=True)),
                ('genres', djongo.models.fields.JSONField()),
                ('screenshots', djongo.models.fields.JSONField(blank=True, null=True)),
                ('movies', djongo.models.fields.JSONField(blank=True, null=True)),
                ('release_date', djongo.models.fields.JSONField(blank=True, null=True)),
                ('background', models.CharField(max_length=100)),
                ('background_raw', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'game',
            },
        ),
        migrations.CreateModel(
            name='NewGame',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('steam_appid', models.IntegerField(primary_key=True, serialize=False)),
                ('required_age', models.IntegerField()),
                ('detailed_description', models.TextField()),
                ('about_the_game', models.TextField()),
                ('short_description', models.TextField()),
                ('header_image', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('pc_requirements', djongo.models.fields.JSONField(blank=True, null=True)),
                ('legal_notice', models.TextField(blank=True, null=True)),
                ('developers', djongo.models.fields.JSONField(blank=True, null=True)),
                ('publishers', djongo.models.fields.JSONField()),
                ('price_overview', djongo.models.fields.JSONField(blank=True, null=True)),
                ('metacritic', djongo.models.fields.JSONField(blank=True, null=True)),
                ('reviewRating', models.CharField(max_length=100, null=True)),
                ('ratingPercent', models.IntegerField(null=True)),
                ('reviewCount', models.IntegerField(null=True)),
                ('categories', djongo.models.fields.JSONField(blank=True, null=True)),
                ('genres', djongo.models.fields.JSONField()),
                ('screenshots', djongo.models.fields.JSONField(blank=True, null=True)),
                ('movies', djongo.models.fields.JSONField(blank=True, null=True)),
                ('release_date', djongo.models.fields.JSONField(blank=True, null=True)),
                ('background', models.CharField(max_length=100)),
                ('background_raw', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'NewGame',
            },
        ),
        migrations.CreateModel(
            name='PopularGame',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('steam_appid', models.IntegerField(primary_key=True, serialize=False)),
                ('required_age', models.IntegerField()),
                ('detailed_description', models.TextField()),
                ('about_the_game', models.TextField()),
                ('short_description', models.TextField()),
                ('header_image', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('pc_requirements', djongo.models.fields.JSONField(blank=True, null=True)),
                ('legal_notice', models.TextField(blank=True, null=True)),
                ('developers', djongo.models.fields.JSONField(blank=True, null=True)),
                ('publishers', djongo.models.fields.JSONField()),
                ('price_overview', djongo.models.fields.JSONField(blank=True, null=True)),
                ('metacritic', djongo.models.fields.JSONField(blank=True, null=True)),
                ('reviewRating', models.CharField(max_length=100, null=True)),
                ('ratingPercent', models.IntegerField(null=True)),
                ('reviewCount', models.IntegerField(null=True)),
                ('categories', djongo.models.fields.JSONField(blank=True, null=True)),
                ('genres', djongo.models.fields.JSONField()),
                ('screenshots', djongo.models.fields.JSONField(blank=True, null=True)),
                ('movies', djongo.models.fields.JSONField(blank=True, null=True)),
                ('release_date', djongo.models.fields.JSONField(blank=True, null=True)),
                ('background', models.CharField(max_length=100)),
                ('background_raw', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'PopularGame',
            },
        ),
        migrations.CreateModel(
            name='surveyQuestion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('question', djongo.models.fields.JSONField()),
            ],
            options={
                'db_table': 'surveyQuestion',
            },
        ),
        migrations.CreateModel(
            name='TopCurrentPlayerGame',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('steam_appid', models.IntegerField(primary_key=True, serialize=False)),
                ('required_age', models.IntegerField()),
                ('detailed_description', models.TextField()),
                ('about_the_game', models.TextField()),
                ('short_description', models.TextField()),
                ('header_image', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('pc_requirements', djongo.models.fields.JSONField(blank=True, null=True)),
                ('legal_notice', models.TextField(blank=True, null=True)),
                ('developers', djongo.models.fields.JSONField(blank=True, null=True)),
                ('publishers', djongo.models.fields.JSONField()),
                ('price_overview', djongo.models.fields.JSONField(blank=True, null=True)),
                ('metacritic', djongo.models.fields.JSONField(blank=True, null=True)),
                ('reviewRating', models.CharField(max_length=100, null=True)),
                ('ratingPercent', models.IntegerField(null=True)),
                ('reviewCount', models.IntegerField(null=True)),
                ('categories', djongo.models.fields.JSONField(blank=True, null=True)),
                ('genres', djongo.models.fields.JSONField()),
                ('screenshots', djongo.models.fields.JSONField(blank=True, null=True)),
                ('movies', djongo.models.fields.JSONField(blank=True, null=True)),
                ('release_date', djongo.models.fields.JSONField(blank=True, null=True)),
                ('background', models.CharField(max_length=100)),
                ('background_raw', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'TopCurrentPlayerGame',
            },
        ),
        migrations.CreateModel(
            name='TopTodayPlayerGame',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('steam_appid', models.IntegerField(primary_key=True, serialize=False)),
                ('required_age', models.IntegerField()),
                ('detailed_description', models.TextField()),
                ('about_the_game', models.TextField()),
                ('short_description', models.TextField()),
                ('header_image', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('pc_requirements', djongo.models.fields.JSONField(blank=True, null=True)),
                ('legal_notice', models.TextField(blank=True, null=True)),
                ('developers', djongo.models.fields.JSONField(blank=True, null=True)),
                ('publishers', djongo.models.fields.JSONField()),
                ('price_overview', djongo.models.fields.JSONField(blank=True, null=True)),
                ('metacritic', djongo.models.fields.JSONField(blank=True, null=True)),
                ('reviewRating', models.CharField(max_length=100, null=True)),
                ('ratingPercent', models.IntegerField(null=True)),
                ('reviewCount', models.IntegerField(null=True)),
                ('categories', djongo.models.fields.JSONField(blank=True, null=True)),
                ('genres', djongo.models.fields.JSONField()),
                ('screenshots', djongo.models.fields.JSONField(blank=True, null=True)),
                ('movies', djongo.models.fields.JSONField(blank=True, null=True)),
                ('release_date', djongo.models.fields.JSONField(blank=True, null=True)),
                ('background', models.CharField(max_length=100)),
                ('background_raw', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'TopTodayPlayerGame',
            },
        ),
        migrations.CreateModel(
            name='UserSteamData',
            fields=[
                ('steamId', models.IntegerField(primary_key=True, serialize=False)),
                ('isPlayTimePublic', models.BooleanField()),
                ('gamePlayTime', djongo.models.fields.ArrayField(model_container=api.models.GamePlayTime, model_form_class=api.models.GamePlayTimeForm)),
            ],
            options={
                'db_table': 'UserSteamData',
            },
        ),
        migrations.CreateModel(
            name='favorite',
            fields=[
                ('appId', models.OneToOneField(db_column='appId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='appId+', serialize=False, to='api.app')),
                ('gameList', djongo.models.fields.JSONField(null=True)),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='surveyResult',
            fields=[
                ('appId', models.OneToOneField(db_column='appId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='appId+', serialize=False, to='api.app')),
                ('result', djongo.models.fields.JSONField()),
            ],
            options={
                'db_table': 'surveyResult',
            },
        ),
        migrations.CreateModel(
            name='recommendationSurvey',
            fields=[
                ('appId', models.OneToOneField(db_column='appId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='appId+', serialize=False, to='api.app')),
                ('R1', models.ForeignKey(blank=True, db_column='R1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1+', to='api.game')),
                ('R10', models.ForeignKey(blank=True, db_column='R10', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R10+', to='api.game')),
                ('R11', models.ForeignKey(blank=True, db_column='R11', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R11+', to='api.game')),
                ('R12', models.ForeignKey(blank=True, db_column='R12', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R12+', to='api.game')),
                ('R13', models.ForeignKey(blank=True, db_column='R13', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R13+', to='api.game')),
                ('R14', models.ForeignKey(blank=True, db_column='R14', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R14+', to='api.game')),
                ('R15', models.ForeignKey(blank=True, db_column='R15', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R15+', to='api.game')),
                ('R16', models.ForeignKey(blank=True, db_column='R16', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R16+', to='api.game')),
                ('R17', models.ForeignKey(blank=True, db_column='R17', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R17+', to='api.game')),
                ('R18', models.ForeignKey(blank=True, db_column='R18', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R18+', to='api.game')),
                ('R19', models.ForeignKey(blank=True, db_column='R19', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R19+', to='api.game')),
                ('R2', models.ForeignKey(blank=True, db_column='R2', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R2+', to='api.game')),
                ('R20', models.ForeignKey(blank=True, db_column='R20', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R20+', to='api.game')),
                ('R3', models.ForeignKey(blank=True, db_column='R3', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R3+', to='api.game')),
                ('R4', models.ForeignKey(blank=True, db_column='R4', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R4+', to='api.game')),
                ('R5', models.ForeignKey(blank=True, db_column='R5', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R5+', to='api.game')),
                ('R6', models.ForeignKey(blank=True, db_column='R6', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R6+', to='api.game')),
                ('R7', models.ForeignKey(blank=True, db_column='R7', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R7+', to='api.game')),
                ('R8', models.ForeignKey(blank=True, db_column='R8', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R8+', to='api.game')),
                ('R9', models.ForeignKey(blank=True, db_column='R9', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R9+', to='api.game')),
            ],
            options={
                'db_table': 'recommendationSurvey',
            },
        ),
    ]