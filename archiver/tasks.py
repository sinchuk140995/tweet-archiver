from django.conf import settings
from django.shortcuts import render

import twitter
import pymongo


def collect_tweets():
    mongo_client = pymongo.MongoClient(settings.MONGO_URL, tz_aware=True)
    db = mongo_client[settings.MONGO_DATABASE_NAME]
    # db.drop_collection(settings.MONGO_COLLECTION_NAME)
    tweets = db[settings.MONGO_COLLECTION_NAME]
    print(f'Tweets count before inserting: {tweets.count_documents({})}')
    tweets.create_index([('tags', pymongo.ASCENDING),
                         ('_id', pymongo.DESCENDING)])

    twitter_api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                              consumer_secret=settings.TWITTER_SECRET_KEY,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    for tag in settings.TAGS:
        tweet_docs = []
        max_tweet_id = tweets.find_one({'tag': tag},
                                       sort=[('_id', pymongo.DESCENDING)])
        if max_tweet_id:
            search_params = {'term': tag,
                             'since_id': max_tweet_id['_id']}
        else:
            search_params = {'term': tag}

        search_results = twitter_api.GetSearch(**search_params)
        print(tag, len(search_results))
        for tweet_status in search_results:
            tweet_doc = tweet_status.AsDict()
            tweet_doc['_id'] = tweet_doc['id']
            tweet_doc['tag'] = tag
            # try:
            #     tweets.insert_one(tweet_doc)
            # except pymongo.errors.DuplicateKeyError:
            #     pass
            tweet_docs.append(tweet_doc)

        if tweet_docs:
            insert_result = tweets.insert_many(tweet_docs)

    print(f'Tweets count after inserting: {tweets.count_documents({})}')
