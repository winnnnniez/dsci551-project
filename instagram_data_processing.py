import pymongo
from pymongo import MongoClient
from pprint import pprint
import requests
import pandas as pd
import sys

def get_collection():
    cluster = MongoClient("mongodb+srv://dbUser:Dsci551project@cluster0.p07da.mongodb.net/dsci551")
    dsci_database = cluster["dsci551"]
    la_post = dsci_database["Instagram_Posts_Collection"]
    # la_post = dsci_database['try']
    return la_post

def coordinates(input_address):
    address = "+".join(input_address.split())
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
        address+",+CA&key=AIzaSyC5Yoip-r1Hy14CzW8nArD7CvOW2uxaXAw"
    geo = requests.get(url)
    if geo.status_code != 200:
        return(None, None)
    coordinates = geo.json()['results'][0]["geometry"]['location']
    lng_lat = [coordinates["lng"], coordinates["lat"]]
    return lng_lat


def sort_by_likes(input_address, collection):
    ret_list = []
    sc = []
    location = coordinates(input_address)
    try:
        for i in collection.find({"loc": {"$near": {"$geometry": {"type":
                                                                  "Point", "coordinates": location},
                                                    "$maxDistance": 3000}}}).sort("number_of_likes",
                                                                                  pymongo.DESCENDING).limit(120):
            # if requests.head(i['display_url']).status_code != 200:
            #     continue
            if i['shortcode'] not in sc:
                post_dict = {}
                post_dict['slug'] = i['slug']
                post_dict['img_url'] = i['display_url']
                post_dict['likes'] = i['number_of_likes']
                post_dict['text'] = i['captions']
                post_dict['time'] = i['timestamp']
                ret_list.append(post_dict)
                sc.append(i['shortcode'])

    except pymongo.errors.OperationFailure:
        for i in collection.find({"loc": {"$near": {"$geometry": {"type":
                                                          "Point", "coordinates": location},
                                            "$maxDistance": 1000}}}).sort("number_of_likes",
                                                                          pymongo.DESCENDING).limit(120):
            # if requests.head(i['display_url']).status_code != 200:
            #     continue
            if i['shortcode'] not in sc:
                post_dict = {}
                post_dict['slug'] = i['slug']
                post_dict['img_url'] = i['display_url']
                post_dict['likes'] = i['number_of_likes']
                post_dict['text'] = i['captions']
                post_dict['time'] = i['timestamp']
                ret_list.append(i)
                sc.append(i['shortcode'])
    return ret_list

def sort_by_date(input_address, collection):
    ret_list = []
    sc = []
    location = coordinates(input_address)
    try:
        for i in collection.find({"loc": {"$near": {"$geometry": {"type":
                                                                  "Point", "coordinates": location},
                                                    "$maxDistance": 3000}}}).sort("timestamp",
                                                                                  pymongo.DESCENDING).limit(120):
            # if requests.head(i['display_url']).status_code != 200:
            #     continue
            if i['shortcode'] not in sc:
                post_dict = {}
                post_dict['slug'] = i['slug']
                post_dict['img_url'] = i['display_url']
                post_dict['likes'] = i['number_of_likes']
                post_dict['text'] = i['captions']
                post_dict['time'] = i['timestamp']
                ret_list.append(post_dict)
                sc.append(i['shortcode'])

    except pymongo.errors.OperationFailure:
        for i in collection.find({"loc": {"$near": {"$geometry": {"type":
                                                          "Point", "coordinates": location},
                                            "$maxDistance": 1000}}}).sort("timestamp",
                                                                          pymongo.DESCENDING).limit(120):
            # if requests.head(i['display_url']).status_code != 200:
            #     continue
            if i['shortcode'] not in sc:
                post_dict = {}
                post_dict['slug'] = i['slug']
                post_dict['img_url'] = i['display_url']
                post_dict['likes'] = i['number_of_likes']
                post_dict['text'] = i['captions']
                post_dict['time'] = i['timestamp']
                ret_list.append(i)
                sc.append(i['shortcode'])
    return ret_list
