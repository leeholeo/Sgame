import io
import requests
import json
from bs4 import BeautifulSoup
import re


CLEANR = re.compile('<.*?>')


def cleanHtml(raw_html):
    if isinstance(raw_html, str):
        cleanText = re.sub(CLEANR, '', raw_html)
        return cleanText


f = io.open('TopGamesSteamspy.html', mode='r', encoding='utf-8')
gameIds = []
for line in f.readlines():
    line = line.strip()
    if 'gameLink' in line:
        startIdx = line.find('/app/') + 5
        target = line[startIdx:startIdx+8]
        target = target[:target.find('"')]
        target = target[:target.find('/')]
        gameIds.append(target)

f.close()
# print(gameIds)

GAME_DETAIL_BASE_URL = 'https://store.steampowered.com/api/appdetails'
keys = [
    'name',
    'steam_appid',
    'required_age',
    'detailed_description',
    'about_the_game',
    'short_description',
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
gameDetails = []
for gameId in gameIds:
    payload = {'appids': gameId, 'l': 'korean'}
    try:
        response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()
    except json.JSONDecodeError:
        print('error occurred!')
        print(len(gameDetails))
        print('error end')
        continue

    response = response[gameId].get('data')
    if not response:
        # 한국어 지원이 안 되는 게임인 경우
        continue
    data = {}
    for key in keys:
        # data[key] = cleanHtml(response.get(key))
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
    gameDetails.append(data)

print(len(gameDetails))
with open("TopGamesSteamspy.json", "w", encoding='utf-8') as jsonFile:
    json.dump(gameDetails, jsonFile, ensure_ascii=False)
