import requests
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/search/?filter=topsellers'
response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
game_ids = []
# loop for all a tags
for link in soup.find_all('a'):
    # get value of attribute "data-ds-appid"
    game_id = link.get('data-ds-appid')
    if game_id:
        # if a game has DLCs, game_id is like "game_id,DLC1_id,DLC2_id"
        game_id = game_id.split(',')[0]
        game_ids.append(game_id)

print(game_ids)

# for game_id in game_ids:
#     game_url = 