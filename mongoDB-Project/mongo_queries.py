import os 
import json 
import re 
import operator
from pymongo import MongoClient
from bson import Binary, Code
from bson.son import SON 
DATABASENAME = 'thejaswini' 
client = MongoClient('localhost', 27017) 
db = client[DATABASENAME] 
X = 89117
Y = 89122
if raw_input("all restaurants in zips ?(type 'yes' to execute)") == 'yes':
    search_zip_codes = {'full_address':{'$regex': "89122" + "|" + "89117"}} 
    result = db.yelp.business.find(search_zip_codes).count()
    print(result)
print"\n"

if raw_input(" all the restaurants in city ?(type 'yes' to execute) ") == 'yes':
    X = str(raw_input("Enter name of the city: ")) 
    search_city = {'city':{'$regex':X,'$options':'-i'}} 
    result=db.yelp.business.find(search_city).count()
    print(result) 
print"\n"
    
if raw_input(" restaurants within 5 miles of lat ,lon?(type 'yes' to execute) ") == 'yes': 
    restuarants = {"loc":{ "$geoWithin":{ "$center":[ [ -80.839186,35.226504] , 5/3963.2 ] } }}
    result=db.yelp.business.find(restuarants).count()
    print(result)
print"\n"
    
if raw_input("all the reviews for restaurant X ?(type 'yes' to execute)") == 'yes':
    review = raw_input("Enter business id for the review: ") 
    review_count={'business_id':review} 
    result=db.yelp.review.find(review_count).count() 
    print(result) 
print"\n"


    
if raw_input("all the reviews for restaurant X that are 5 stars?(type 'yes' to execute)") == 'yes':    
	review = raw_input("Enter business id for the review: ") 
	result=db.yelp.review.find({"business_id":review ,"stars":5}).count() 
	print(result)
print"\n"


	
if raw_input("all the users that have been yelping for over 5 years?(type 'yes' to execute)") == 'yes': 
   yelp={"yelping_since" : { "$gt" : "2011-17"}}
   result = db.yelp.user.find(yelp).limit(5)
   for r in result:
        print(r)
print"\n"

   
if raw_input("the business that has the tip with the most likes?(type 'yes' to execute)") == 'yes': 
   result = db.yelp.tip.find().sort('likes',-1).limit(1)
   for r in result:
        print(r)
print"\n"


if raw_input("the average review_count for users?(type 'yes' to execute)") == 'yes': 
   result = db.yelp.user.aggregate([{"$group": {"_id":0, 'avg_review_count': {"$avg":"$review_count"} } }])
   for r in result:
   		print(r)
print"\n"
   
if raw_input("all the users that are considered elite?(type 'yes' to execute)") == 'yes': 
   result = db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).count()
   print(result)
print"\n"
  
if raw_input("the longest elite user?(type 'yes' to execute)") == 'yes': 
   result = db.yelp.user.aggregate( [{ "$unwind" : "$elite" },{ "$group" : { "_id" : "$_id", "duration" : { "$sum" : 1 }} },{ "$sort" : { "duration" : -1 } },{ "$limit" : 1 }] )
   for r in result:
        print(r)
print"\n"

