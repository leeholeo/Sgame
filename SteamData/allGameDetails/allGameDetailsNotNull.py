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

allGameDetails = {}
for unit in range(10):
    with open(f'allGameDetails/allGameDetails{unit}.pkl', 'rb') as f:
        unitGameDetails = pickle.load(f)
    
    for gameId in unitGameDetails.keys():
        for jsonFieldKey in jsonFieldKeys:
            if not unitGameDetails[gameId].get(jsonFieldKey):
                unitGameDetails[gameId][jsonFieldKey] = {}

        allGameDetails[gameId] = unitGameDetails[gameId]

with open(f"allGameDetails/allGameDetails.pkl", "wb") as f:
    pickle.dump(allGameDetails, f)

print(f'{len(allGameDetails)}')

