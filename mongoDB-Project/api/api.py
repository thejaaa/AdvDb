from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

import json
import urllib


import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)
db = client['thejaswini']
businessdb = db['yelp.business']
review = db['yelp.review']
userdb = db['yelp.user']
tipdb = db['yelp.tip']


parser = reqparse.RequestParser()

"""=================================================================================="""
"""=================================================================================="""
"""=================================================================================="""


@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

   
"""=================================================================================="""
1
"""=================================================================================="""
@app.route("/zip/<args>", methods=['GET'])
def zip(args):
    """finding all restuarant users with zip codes x or y"""
    args = myParseArgs(args)

    args['zips']=args['zips']
    zipcode=args['zips'].split(',')
    a=zipcode[0]
    zip1 = '.*' + a +'.*'
    b=zipcode[1]
    zip2='.*' + b +'.*'

    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])    
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({'$or': [{'full_address' : {'$regex' : zip1 }},{'full_address' : {'$regex' : zip2}}]},{"full_address":1,"name":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find({'$or': [{'full_address' : {'$regex' : zip1}},{'full_address' : {'$regex' : zip2}}]},{"full_address":1,"name":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find({'$or': [{'full_address' : {'$regex' : zip1}},{'full_address' : {'$regex' : zip2}}]},{"full_address":1,"name":1,"_id":0}).limit(args['limit'])
    else:
        result = businessdb.find({'$or': [{'full_address' : {'$regex' : zip1}},{'full_address' : {'$regex' : zip2}}]},{"full_address":1,"name":1,"_id":0}).limit(10)  
    
    
    for r in result:
        data.append(r)
    return {"resturants with zips x,y":data}
   
"""=================================================================================="""
2
"""=================================================================================="""
@app.route("/city/<args>", methods=['GET'])
def city(args):
    """finding all restuarnts in city x"""
    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    city=args['city']

    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({'full_address':{'$regex':city}},{"full_address":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find({'full_address':{'$regex':city }},{"full_address":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find({'full_address':{'$regex':city }},{"full_address":1,"_id":0}).limit(args['limit'])
    else:
        result = businessdb.find({'full_address':{'$regex':city }},{"full_address":1,"_id":0}).limit(10)  
    
    
    for r in result:
        data.append(r)

    return {" resturants in city x":data}
"""=================================================================================="""
3
"""=================================================================================="""
@app.route("/closest/<args>", methods=['GET'])
def closest(args):
    """finding all restaurants  between 5 miles of lat,lon"""
    args = myParseArgs(args)

    args['lon']=float(args['lon'])
    args['lat']=float(args['lat'])
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])    
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({ 'loc' : { '$geoWithin' : { '$centerSphere': [ [ args['lon'],args['lat' ]], 5 / 3963.2 ] } } },{"name":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find({ 'loc' : { '$geoWithin' : { '$centerSphere': [ [ args['lon'],args['lat' ]], 5 / 3963.2 ] } } },{"name":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find({ 'loc' : { '$geoWithin' : { '$centerSphere': [ [ args['lon'],args['lat' ]], 5 / 3963.2 ] } } },{"name":1,"_id":0}).limit(args['limit'])
    else:
        result = businessdb.find({ 'loc' : { '$geoWithin' : { '$centerSphere': [ [ args['lon'],args['lat' ]], 5 / 3963.2 ] } } },{"name":1,"_id":0}).limit(10)  
    
    
    for r in result:
        data.append(r)
    return {"restaurants within 5 miles of lat,lon ":data}
   
    
	
	
"""=================================================================================="""
4	
"""=================================================================================="""
@app.route("/reviews/<args>", methods=['GET'])
def reviews(args):
    """Finding all the reviews for restaurant X"""
    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    #.start(1).limit(1)    
    id = args['id']
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find({'business_id':id},{"id":1,"user_id":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = review.find({'business_id':id},{"id":1,"user_id":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = review.find({'business_id':id},{"id":1,"user_id":1,"_id":0}).limit(args['limit'])
    else:
        result = review.find({'business_id':id},{"id":1,"user_id":1,"_id":0}).limit(10)

    for r in result:
        data.append(r)	

    return {"reviews for restaurant x":data}
"""=================================================================================="""
5
"""=================================================================================="""
@app.route("/stars/<args>", methods=['GET'])
def stars(args):
    """finding all the reviews of restuarant x that are of 5 stars."""
    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    args ['id'] = args ['id']
    args ['num_stars']=int(args['num_stars'])
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find({'business_id' : args['id'],'stars' : args['num_stars']},{"review_id":1,"stars":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = review.find({'business_id' : args['id'],'stars' : args['num_stars']},{"review_id":1,"stars":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = review.find({'business_id' : args['id'],'stars' : args['num_stars']},{"review_id":1,"stars":1,"_id":0}).limit(args['limit'])
    else:
        result = review.find({'business_id' : args['id'],'stars' : args['num_stars']},{"review_id":1,"stars":1,"_id":0}).limit(10)  
    for r in result:
        data.append(r)

    return {"reviews for 5 star":data}
"""=================================================================================="""
6
"""=========================================================================="""
@app.route("/yelping/<args>", methods=['GET'])
def yelping(args):
    """Finding all the users that have been yelping for over 5 years"""
    args = myParseArgs(args)
    min_years = int(args['min_years'])
    new=2016
    old_year= new - min_years
    month=12
    year=str(old_year) + "-" + str(month)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []

    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({ 'yelping_since' : {'$gte':year}}, {"_id":0,"name":1}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({ 'yelping_since' : {'$gte':year}}, {"_id":0,"name":1}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({ 'yelping_since' : {'$gte':year}}, {"_id":0,"name":1}).limit(args['limit'])
    else:
        result = userdb.find({ 'yelping_since' : {'$gte':year}}, {"_id":0,"name":1}).limit(10)  
    for r in result:
        data.append(r)

    return {"users yelping over 5 years":data}      
    
    

"""=================================================================================="""
7
"""=================================================================================="""
@app.route("/most_likes/<args>", methods=['GET'])
def most_likes(args):
    """Finding the business that has the tip with the most likes"""
    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = tipdb.find({},{"business_id":1,"_id":0,"likes":1}).sort([('likes' , -1)]).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = tipdb.find({},{"business_id":1,"_id":0,"likes":1}).sort([('likes' , -1)]).skip(args['start'])
    elif 'limit' in args.keys():
        result = tipdb.find({},{"business_id":1,"_id":0,"likes":1}).sort([('likes' , -1)]).limit(args['limit'])
    else:
        result = tipdb.find({},{"business_id":1,"_id":0,"likes":1}).sort([('likes' , -1)]).limit(10)  
    for r in result:
        data.append(r)

    return {"business that has tip with most likes are":data}
    
    

"""=================================================================================="""
8
"""=================================================================================="""
@app.route("/review_count/", methods=['GET'])
def review_count():
    """finding average review_count for users"""
  
    data = []

    result = userdb.aggregate([{"$group":{"_id":"review_count","averageReviewCount":{"$avg":"$review_count"}}}])
    for r in result:
        data.append(r['averageReviewCount'])
    return {" average review_count":data}
"""=================================================================================="""
9
"""=================================================================================="""
@app.route("/elite/<args>", methods=['GET'])
def elite(args):
    """finding all the users that are considered elite"""
    args = myParseArgs(args)

    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []

    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({'elite':{'$ne':[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({'elite':{'$ne':[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({'elite':{'$ne':[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(args['limit'])
    else:
        result = userdb.find({'elite':{'$ne':[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(10)  


    for r in result:
        data.append(r)
    return {"users that are elite":data}
"""=================================================================================="""
10
"""=================================================================================="""
@app.route("/elite_longest/<args>", methods=['GET'])
def elite_longest(args):
    """finding the longest elite user"""
    args = myParseArgs(args)

    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({"elite":{'$ne':[]}},{"_id":0,"name":1,"elite":1}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({"elite":{'$ne':[]}},{"_id":0,"name":1,"elite":1}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({"elite":{'$ne':[]}},{"_id":0,"name":1,"elite":1}).limit(args['limit'])
    else:
        result = userdb.find({"elite":{'$ne':[]}},{"_id":0,"name":1,"elite":1}).limit(1)  


    for r in result:
        data.append(r)
    return {"longest elite user":data}
"""=================================================================================="""
11
"""=================================================================================="""
@app.route("/avg_elite/", methods=['GET'])
def avg_elite():
    """finding the average number of years someone is elite in elite users"""
    data = []
		
    result = userdb.aggregate([{'$project': {'elitelength':{'$size':"$elite"}}},{'$group':{"_id":None, 'avgYears':{'$avg':"$elitelength"}}}])
    
    for row in result:
        data.append(row)
    
    return {"average elite user":data}
"""=================================================================================="""
@app.route("/user/<args>", methods=['GET'])
def user(args):

    args = myParseArgs(args)
    
    if 'skip' in args.keys():
        args['skip'] = int(args['skip'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    
    #.skip(1).limit(1)
    
    if 'skip' in args.keys() and 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip']).limit(args['limit'])
    elif 'skip' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip'])
    elif 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).limit(args['limit'])
    else:
        result = userdb.find({},{'_id':0}).limit(10)  

    for row in result:
        data.append(row)


    return {"data":data}
    

	

@app.route("/business/<args>", methods=['GET'])
def business(args):

    args = myParseArgs(args)
    
    data = []
    
    result = businessdb.find({},{'_id':0}).limit(100)
    
    for row in result:
        data.append(row)
    

    return {"data":data}
"""=================================================================================="""
def snap_time(time,snap_val):
    time = int(time)
    m = time % snap_val
    if m < (snap_val // 2):
        time -= m
    else:
        time += (snap_val - m)
        
    if (time + 40) % 100 == 0:
        time += 40
        
    return int(time)

"""=================================================================================="""
def myParseArgs(pairs=None):
    """Parses a url for key value pairs. Not very RESTful.
    Splits on ":"'s first, then "=" signs.
    
    Args:
        pairs: string of key value pairs
        
    Example:
    
        curl -X GET http://cs.mwsu.edu:5000/images/
        
    Returns:
        json object with all images
    """
    
    if not pairs:
        return {}
    
    argsList = pairs.split(":")
    argsDict = {}

    for arg in argsList:
        key,val = arg.split("=")
        argsDict[key]=str(val)
        
    return argsDict
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
