# from cgitb import text
# import requests



# url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=F0B488C9E39737CF0BD0270321060EB8&vanityurl=KraQuenz'
# response = requests.get(url).text
# print(response)
# print(type(None))
# A = {1, 2, 3, 4, 5, 6, 7, 8}
# for a in A:
#     if a % 2:
#         A.remove(a)

# b = 0
# c = 1
# a = f'{b} {c}'
# print(a)
# b = 123
# c = 124134
# print(a)


# import pickle


# with open(r'userGames/allGameIds.pkl', 'rb') as f:
#     # uesrIds는 set 자료형이다.
#     userGames = pickle.load(f)


# print(len(userGames))

# from bs4 import BeautifulSoup
# import requests
# gameId = '1245620'
# key = '123'
# payload = { 'appids': gameId, 'l': 'korean' }
# GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'
# response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()[gameId]
# print(response.get(key))
# print(BeautifulSoup(response.get(key), 'html.parser').get_text())


# import pickle

# # # with open(r'userGames/userGamesPlayTimePublic.pkl', 'rb') as f:
# # #     userGames = pickle.load(f)

# # # print(userGames)


# # with open(r'topCurrentPlayerGames/topCurrentPlayerGames.pkl', 'rb') as f:
# #     allGameIds = pickle.load(f)

# # for gameId in allGameIds:
# #     print(gameId['name'])
# # print(len(allGameIds))
# # print(allGameIds)

# with open('gameReviews/userIdsFromGameReviews.pkl', 'rb') as f:
#     userGames = pickle.load(f)

# print(len(userGames))

a = [1, 2, 3, '4', '5', '6']
for aa in a:
    print(f'aa{aa}aa')

# import json

# print(json.loads('{}'))

# print(' '.isdigit())

# import requests
# from bs4 import BeautifulSoup

# GAMES_CRAWLING_BASE_URL = 'https://store.steampowered.com/app/'
# GAME_DETAIL_BASE_URL = 'http://store.steampowered.com/api/appdetails/'
# KEYS = [
#     'name',
#     'steam_appid',
#     'required_age',
#     'detailed_description',
#     'about_the_game',
#     'short_description',
#     'supported_languages',
#     'header_image',
#     'website',
#     'pc_requirements',
#     'legal_notice',
#     'developers',
#     'publishers',
#     'price_overview',
#     'metacritic',
#     'categories',
#     'genres',
#     'screenshots',
#     'movies',
#     'release_date',
#     'background',
#     'background_raw'
# ]

# def a(gameId):
#     payload = { 'l': 'korean' }

#     try:
#         response = requests.get(GAMES_CRAWLING_BASE_URL + gameId, params=payload).text
#     except Exception as e:
#         print(f'Error occurred! Error: {e}')
#         return f'Error occurred! Error: {e}'

#     soup = BeautifulSoup(response, 'html.parser')

#     reviewRating = ''
#     reviewCount = -1
#     ratingPercent = -1
#     for link in soup.find_all('div', attrs={ 'class': 'user_reviews_summary_row' }):
#         subtitle = link.find('div', attrs={ 'class': 'subtitle' }).get_text()
#         if subtitle != '모든 평가':
#             continue
        
#         spans = link.find('div', attrs={ 'class': 'summary' }).find_all('span')
#         if len(spans) < 2:
#             continue

#         if spans[1].get('class') != ['responsive_reviewdesc_short']:
#             continue
        
#         reviewRating = spans[0].get_text()
#         reviewRaw = spans[1].get_text().strip()
#         reviewCount = reviewRaw[reviewRaw.find('/') + 1:reviewRaw.find(')')].replace(',', '')
#         ratingPercent = reviewRaw[1:reviewRaw.find('%')].replace(',', '')

#         if reviewCount.isdigit() and ratingPercent.isdigit():
#             return {
#                 'reviewRaw' : reviewRating,
#                 'reviewCount' : int(reviewCount),
#                 'ratingPercent' : int(ratingPercent)
#             }
#         else:
#             pass
    
#     return f'Rating data cannot found'

# def b(gameId):
#     payload = { 'appids': gameId, 'l': 'korean' }
#     try:
#         response = requests.get(GAME_DETAIL_BASE_URL, params=payload).json()
#     except Exception as e:
#         print(f'Error occurred! Error: {e}')
#         return f'Error occurred! Error: {e}'
        
#     if not response:
#         return 'No response!'

#     response = response[gameId]
#     if response['success'] == False:
#         # 한국어 지원이 안 되는 게임인 경우
#         return 'Korean not supported'

#     response = response.get('data')
#     if response['type'] != 'game':
#         return 'Not a game'

#     data = {}
#     for key in KEYS:
#         dataItem = response.get(key)
#         if isinstance(dataItem, str) and dataItem[:4] != 'http':
#             data[key] = BeautifulSoup(response.get(key), 'html.parser').get_text()
#         elif isinstance(dataItem, dict):
#             for k, v in dataItem.items():
#                 if isinstance(v, str) and v[:4] != 'http':
#                     dataItem[k] = BeautifulSoup(v, 'html.parser').get_text()
#                 else:
#                     dataItem[k] = v
#             data[key] = dataItem
#         else:
#             data[key] = dataItem
    
#     return data


# print(a('20'))
# print(b('20'))