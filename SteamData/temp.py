import requests
from bs4 import BeautifulSoup

app_id = 1245620
url = f'https://steamcommunity.com/app/{app_id}/reviews/?browsefilter=toprated&snr=1_5_100010_'
response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
print(soup)
game_ids = ['']
for link in soup.find_all('a'):
    # get value of attribute "href"
    game_id = link.get('href')
    if game_id[:30] == 'https://steamcommunity.com/id/' or game_id[:36] == 'https://steamcommunity.com/profiles/':
        # two types of user profile urls
        if game_id == game_ids[-1]:
            # a tag linked to user profile repeated twice, ignore it
            continue

        game_ids.append(game_id)

game_ids.pop(0)
print(game_ids)
