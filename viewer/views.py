from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

import pymongo


mongo_client = pymongo.MongoClient(settings.MONGO_URL, tz_aware=True)
db = mongo_client[settings.MONGO_DATABASE_NAME]
tweets_collection = db[settings.MONGO_COLLECTION_NAME]


class IndexView(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('tag'):
            selector = {'tag': request.GET['tag']}
        else:
            selector = {}
        found_tweets = tweets_collection.find(selector,
                                              sort=[('_id', pymongo.DESCENDING)])
        context = {
            'tags': settings.TAGS,
            'tweets': found_tweets,
        }
        return render(request, 'index.html', context)
