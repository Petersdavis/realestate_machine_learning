

# importing the requests library 
import requests
import json
import realtorca
import database
import locations
import randomSleep
import time

while(True):
  time.sleep(6)
  db = database.connect()
  activeListings = database.getActiveListings(db)

  results = []
  for location in locations.locations:
    print("Searching in Location:", location)
    randomSleep.sleep(1)
    locationName = location["name"]
    results = results + realtorca.searchRealEstate(location["lat"], location["long"], 1)
  parsedResults = list(map(realtorca.parseResult, results))
  Listings, Events = database.compareResultsToActiveListings(results, activeListings)

  database.upsertListings(Listings, db)
  database.insertEvents(Events, db)
  print("got Events", len(Events), "Got Listings", len(Listings))
  db.close()
  randomSleep.sleep(173800)

