import mysql.connector
def connect():
  mydb = mysql.connector.connect(
    host="localhost",
    user="test",
    passwd="test123",
    database="realestate",
    autocommit=True
  )
  return mydb

def upsertListings(listings, db):
  try:
    cursor = db.cursor(prepared=True)
    sql = """ INSERT INTO listings
                        (listingId, mlsId, bedroom, bathroom, story, type, price, parking, addressString, addressLong, addressLat, area, ownership, postal, active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `active` = Values(`active`), `price` = Values(`price`)"""  
   
    tups = []
    for listing in listings:
      tups.append((
        listing["listingId"],
        listing["mlsId"],
        listing["bedroom"],
        listing["bathroom"],
        listing["story"],
        listing["type"],
        listing["price"],
        listing["parking"],
        listing["addressString"],
        listing["addressLong"],
        listing["addressLat"],
        listing["area"],
        listing["ownership"],
        listing["postal"],
        listing["active"],
      ))
    cursor.executemany(sql, tups)
    db.commit
    print(cursor.rowcount, "record inserted.")
    print(len(listings))
  except mysql.connector.Error as error:
    print("parameterized query failed {}".format(error))
  finally:
    if (db.is_connected()):
      cursor.close()



def getActiveListings(db):
  cursor = db.cursor()
  result=cursor.execute("select listingId, mlsId, bedroom, bathroom, story, type, price, parking, addressString, addressLong, addressLat, area, ownership, postal, active, _createdAt from listings WHERE active = 1")
  data = cursor.fetchall()
  data= list(map(lambda x: {
    'listingId':x[0],
    'mlsId':x[1],
    'bedroom':x[2],
    'bathroom':x[3],
    'story':x[4],
    'type':x[5],
    'price':x[6],
    'parking':x[7],
    'addressString':x[8],
    'addressLong':x[9],
    'addressLat':x[10],
    'area':x[11],
    'ownership':x[12],
    'postal':x[13],
    'active':x[14],
    '_createdAt':x[15]
  }, data))
  cursor.close()
  return data

def compareResultsToActiveListings(results, activeListing):
  newListings =[]
  closedListings=[]
  modifiedListings=[]
  listingEvents =[]

  for record in results:
    foundExistingRecord = False
    for listing in activeListing:
      if(record['mlsId'] == listing['mlsId']):
        foundExistingRecord = True
        if(record['price'] != listing['price']):
          modifiedListings.append(record)
          if(record['price'] > listing['price']):
            listingEvents.append({'type':"INCREASE_PRICE", 'mlsId':record['mlsId'] })
          else:
            listingEvents.append({'type':"DECREASE_PRICE", 'mlsId':record['mlsId'] })
    
    if not foundExistingRecord:
      newListings.append(record)
      listingEvents.append({'type':"NEW_LISTING", 'mlsId':record['mlsId'] })

  for listing in activeListing:
    listingStillExists = False
    for record in results:
      if(record['mlsId'] == listing['mlsId']):
        listingStillExists = True
    if not listingStillExists:
      listing.active = 0
      closedListings.append(listing) 
      listingEvents.append({'type':"CLOSED_LISTING", 'mlsId':record['mlsId'] })



  return newListings, closedListings, modifiedListings, listingEvents

#def getListingsDiff(currentListings, activeListings):








