import pymongo
from pymongo import MongoClient
import requests
import pandas as pd

def get_collection():
    cluster = MongoClient("mongodb+srv://dbUser:Dsci551project@cluster0.p07da.mongodb.net/dsci551")
    dsci_database = cluster["dsci551"]
    la_res = dsci_database["LA_restaurants"]
    return la_res

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

def groupByPrice(res):
    res_df = pd.DataFrame(res)
    price_dict = res_df.pivot_table(index="price", aggfunc='size').to_dict()
    price_list = sorted(price_dict.items(), key=lambda x: x[0])
    return price_list

def groupByRating(res):
    res_df = pd.DataFrame(res)
    rating_dict = res_df.pivot_table(index="rating", aggfunc='size').to_dict()
    rating_list = sorted(rating_dict.items(), key=lambda x: x[0], reverse=True)
    return rating_list

def groupByCategory(res):
    res_df = pd.DataFrame(res)
    category_dict = res_df.pivot_table(index="categories", aggfunc='size').to_dict()
    sorted(category_dict.items(), key=lambda x: x[1], reverse=True)
    category_list = sorted(category_dict.items(), key=lambda x: x[1], reverse=True)
    return category_list

def groupByPriceRatingCategory(input_address, collection):
    res_list = get_res_info(input_address, collection)
    if res_list != []:
        ret_list = list()
        price = groupByPrice(res_list)
        rating = groupByRating(res_list)
        category = groupByCategory(res_list)
    return price, rating, category

def get_res_info(input_address, collection):
    ret_list = []
    location = coordinates(input_address)
    for i in collection.aggregate([{"$geoNear": {"near": {"type": "Point",
                                                      "coordinates": location},
                                             "maxDistance": 1000, "spherical": "true",
                                             "distanceField": "distance",
                                             "distanceMultiplier": 0.000621371}}, {"$sort": {"distance": 1}}]):
        res_dict = {}
        res_dict['name'] = i["name"]
        res_dict['categories'] = i["categories"]
        res_dict['rating'] = i['rating']
        res_dict['price'] = i['price']
        res_dict['address'] = i['address'][0]
        res_dict['img_url'] = i['image_url']
        res_dict['map_src'] = (i['address'][0]+i["name"]).replace(' ', '+').replace('&', '+')
        ret_list.append(res_dict)
    return ret_list

def get_filtered_res(input_address, collection, filters):
    ret_list = []
    location = coordinates(input_address)
    for i in collection.aggregate([{"$geoNear": {"near": {"type": "Point",
                                                      "coordinates": location},
                                             "maxDistance": 1000, "spherical": "true",
                                             "distanceField": "distance",
                                             "distanceMultiplier": 0.000621371}}, {"$sort": {"distance": 1}}]):
        res_dict = {}
        a, b, c = 1, 1, 1
        if filters[0]:
            a = str(i['rating']) in filters[0]
        if filters[1]:
            b = i['price'] in filters[1]
        if filters[2]:
            c = i['categories'] in filters[2]
        if a and b and c:
            res_dict['name'] = i["name"]
            res_dict['categories'] = i["categories"]
            res_dict['rating'] = i['rating']
            res_dict['price'] = i['price']
            res_dict['address'] = i['address'][0]
            res_dict['img_url'] = i['image_url']
            res_dict['map_src'] = (i['address'][0]+i["name"]).replace(' ', '+').replace('&', '+')
            ret_list.append(res_dict)
    return ret_list
