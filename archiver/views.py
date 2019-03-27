from django.conf import settings
from django.shortcuts import render

import twitter

from pymongo import MongoClient


def collect_tweets():
    connection = MongoClient(settings.MONGO_URL, tz_aware=True)
    print(connection)
    db = client[settings.MONGO_DATABASE_NAME]
    tweets = db[settings.MONGO_COLLECTION_NAME]
    tweets.create_index([('tags', pymongo.ASCENDING),
                         ('_id', pymongo.DESCENDING)])

    twitter_api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                              consumer_secret=settings.TWITTER_SECRET_KEY,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    print(twitter_api)
