from django.conf import settings
from django.shortcuts import render

import twitter
import pymongo


def collect_tweets():
    connection = pymongo.MongoClient(settings.MONGO_URL, tz_aware=True)
    # print(connection)
    db = connection[settings.MONGO_DATABASE_NAME]
    tweets = db[settings.MONGO_COLLECTION_NAME]
    print(f'Tweets count before inserting: {tweets.count_documents({})}')
    tweets.create_index([('tags', pymongo.ASCENDING),
                         ('_id', pymongo.DESCENDING)])

    twitter_api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                              consumer_secret=settings.TWITTER_SECRET_KEY,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    # print(twitter_api)
    for tag in settings.TAGS:
        tweet_docs = []
        max_tweet_id = tweets.find_one(sort=[('_id', pymongo.DESCENDING)])
        search_results = twitter_api.GetSearch(term=tag,
                                               since_id=max_tweet_id['_id'])
        for tweet_status in search_results:
            tweet_doc = tweet_status.AsDict()
            tweet_doc['_id'] = tweet_doc['id']
            tweet_doc['tags'] = [tag]
            # try:
            #     tweets.insert_one(tweet_doc)
            # except pymongo.errors.DuplicateKeyError:
            #     pass
            tweet_docs.append(tweet_doc)

        if len(tweet_docs):
            insert_result = tweets.insert_many(tweet_docs)

    print(f'Tweets count after inserting: {tweets.count_documents({})}')
