import requests
import json
import randomSleep
import re


def parseInt(text):
  result = 0
  if text == "":
    return 0
  parts = text.split("+")
  for part in parts:
    result = result + int(float(re.sub('[^0-9/.]','', part)))
  return result

def parseFloat(text):
  result = 0
  if text == "":
    return 0
  parts = text.split("+")
  for part in parts:
    result = result + float(re.sub('[^0-9/.]','', part))
  return result

def parseResult(data):
  Building = data.get("Building", {})
  Property = data.get("Property", {})
  Address = Property.get("Address", {})

  return {
    "listingId":data.get("Id"),
    "mlsId":data.get("MlsNumber"),
    "bedroom":parseFloat(Building.get("Bedrooms", "")),
    "bathroom":parseFloat(Building.get("BathroomTotal", "")),
    "story":parseFloat(Building.get("StoriesTotal", "")),
    "type":Building.get("Type"),
    "price":parseInt(Property.get("Price")),
    "parking":Property.get("ParkingSpaceTotal", ""),
    "addressString":Address.get("AddressText", "") ,
    "addressLong":parseFloat(Address.get("Longitude", "")),
    "addressLat":parseFloat(Address.get("Latitude", "")),
    "area":parseInt(Building.get("SizeInterior", "")),
    "ownership":Property.get("OwnershipType"),
    "postal":data.get("PostalCode"),
    "active":1
  }

def searchRealEstate(targetLat, targetLong, page):
  # api-endpoint 
  URL = "https://api2.realtor.ca/Listing.svc/PropertySearch_Post"
  latMax = targetLat + 0.1
  latMin = targetLat - 0.1
  longMax = targetLong + 0.1
  longMin = targetLong - 0.1
  data = {
      'ZoomLevel':12,
      'LatitudeMax':latMax,
      'LongitudeMax':longMax,
      'LatitudeMin':latMin,
      'LongitudeMin':longMin,
      'Sort':'1-A',
      'PropertyTypeGroupID':1,
      'PropertySearchTypeId':1,
      'TransactionTypeId':2,
      'Currency':'CAD',
      'RecordsPerPage':200,
      'ApplicationId':1,
      'CultureId':1,
      'Version':7.0,
      'CurrentPage':page
  } 
  headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "api2.realtor.ca",
    "Origin": "https://www.realtor.ca",
    "Referer": "https://www.realtor.ca/map",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
  }

  # sending post request and saving response as response object 
  r = requests.post(url = URL, data = data, headers=headers) 

  # extracting data in json format 
  y = r.json()

  results = y["Results"]
  
  countResults = int(y["Paging"]["TotalRecords"])
  recordsPerPage = int(y["Paging"]["RecordsPerPage"])
  remainingResults = countResults-(recordsPerPage * page)
  print("Fetched Results", countResults)
  print("Remaining Results", remainingResults)
  
  if remainingResults > 0:
    randomSleep.sleep(10)
    results = results + searchRealEstate(targetLat, targetLong, page + 1)
  
  return results




