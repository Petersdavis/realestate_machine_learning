

# importing the requests library 
import requests
import json
import realtorca
import database
import locations
import randomSleep

with open('./sample.json') as f:
  data = json.load(f)

parsedData = list(map(realtorca.parseResult, data))

db = database.connect()
activeListings = database.getActiveListings(db)

results = []
for location in locations.locations:
  randomSleep.sleep(1)
  locationName = location["name"]
  results = results + realtorca.searchRealEstate(location["lat"], location["long"], 1)

newListings, missingListings, modifiedListings, listingEvents = database.compareResultsToActiveListings(results, activeListings)
print(data[0])

