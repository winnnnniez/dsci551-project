import findspark
findspark.init()
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from pyspark import SparkContext, SparkConf
import pyspark
from pymongo import MongoClient
import pymongo
import functools
import operator
import schedule
import time
import datetime
from datetime import datetime

conf = SparkConf().setAppName("Fetching App").setMaster("local[4]")
sc = SparkContext(conf=conf)

def fetch_newest_post(location):
    location = str(location)
    url = "https://instagram47.p.rapidapi.com/location_posts"

    querystring = {"locationid":location}

    headers = {
    'x-rapidapi-key': "13807db56cmsh073d74d4807d705p1e9022jsnbb9b7c8e194e",
    'x-rapidapi-host': "instagram47.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def cleaned_data_ready_to_upload(location):
    ins = fetch_newest_post(location)
    filtered_posts = []
    print(location)
    try:
        slug = ins["body"]["slug"]
        location_id = ins["body"]["id"]
        loc = {"type":"Point","coordinates":[ins["body"]["lng"],ins["body"]["lat"]]}
        for i in ins["body"]["edge_location_to_top_posts"]["edges"]:
            info = {"location_id":location_id,"slug":slug,"loc":loc}
            if i["node"]["edge_media_to_caption"]["edges"]!= {}:
                info["captions"] = i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            else:
                info["captions"] = "No Captions Provided"
            info["display_url"] = i["node"]["display_url"]
            info["shortcode"] = i["node"]["shortcode"]
            info["number_of_likes"] = i["node"]["edge_liked_by"]["count"]
            info["timestamp"] = datetime.fromtimestamp(i["node"]["taken_at_timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            filtered_posts.append(info)
    except:
        return ("Instagram API is not working currently, please wait for at least 5 mins...")
    return filtered_posts

def uploading():
    print("ready to fetch new posts")
    ##1774116282901667(little tokyo),1152951608161154 (santamonica),214519628(la-ktown),238434635(usc-rose garden)
    #location_list = [349029876,1774116282901667,1152951608161154,214519628,238434635]
    location_list = [1639313,1273538]
    location_rdd = sc.parallelize(location_list)
    print("finished prallelizing")
    post_rdd = location_rdd.map(cleaned_data_ready_to_upload)
    print("finished mapping")
    cluster = MongoClient("mongodb+srv://dbUser:Dsci551project@cluster0.p07da.mongodb.net/dsci551")
    db = cluster["dsci551"]
    flat_list_rdd= functools.reduce(operator.iconcat,post_rdd.collect(), [])
    for li in flat_list_rdd:
        try:
            db["Instagram_Posts_Collection"].insert_one(li)
        except:
            pass
    print("Posts have been updated!!")
    with open("cnt.txt", "w+") as f:
        data = f.read()
        if not data:
            f.write("1")
        else:
            f.write(int(data) + 1)

def fetch_every_3_mins():
    scheduler = BackgroundScheduler()
    scheduler.add_job(uploading, 'interval', minutes=3)
    scheduler.start()

if __name__ == '__main__':
    schedule.every(60).minutes.do(uploading)
    while True:
        schedule.run_pending()
        time.sleep(1)
