import pickle

# 2. 게임 id 크롤링, bs4여도 상관이 없다
allGameRatings = {}
for unit in range(10):
    with open(f'gameRatings/gameRatings{unit}.pkl', 'rb') as f:
        gameRatings = pickle.load(f)
    
    for gameId, rating in gameRatings.items():
        allGameRatings[gameId] = rating

print(len(allGameRatings))
with open(f"gameRatings/gameRatings.pkl", "wb") as f:
    pickle.dump(allGameRatings, f)