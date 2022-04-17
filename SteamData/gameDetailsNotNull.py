import pickle


jsonFieldKeys = [
    'pc_requirements',
    'developers',
    'price_overview',
    'metacritic',
    'categories',
    'screenshots',
    'movies',
    'release_date'
]

# newGameDetails = {}
# with open(f'topCurrentPlayerGames/topTodayPlayerGames.pkl', 'rb') as f:
#     targetGameDetails = pickle.load(f)

# for gameId in targetGameDetails.keys():
#     for jsonFieldKey in jsonFieldKeys:
#         if not targetGameDetails[gameId].get(jsonFieldKey):
#             targetGameDetails[gameId][jsonFieldKey] = {}

#     newGameDetails[gameId] = targetGameDetails[gameId]

# with open(f"topCurrentPlayerGames/topTodayPlayerGames.pkl", "wb") as f:
#     pickle.dump(newGameDetails, f)

# print(f'{len(newGameDetails)}')

topSellers = []
with open(f'topSellers/topSellers.pkl', 'rb') as f:
    targetGameDetails = pickle.load(f)

for idx in range(len(targetGameDetails)):
    for jsonFieldKey in jsonFieldKeys:
        if not targetGameDetails[idx].get(jsonFieldKey):
            targetGameDetails[idx][jsonFieldKey] = {}

    topSellers.append(targetGameDetails[idx])

with open(f"topSellers/topSellers.pkl", "wb") as f:
    pickle.dump(topSellers, f)

print(f'{len(topSellers)}')
