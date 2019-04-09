import os
import random

import tweepy
from django.http import JsonResponse


def user_toxicity(request, user_id):

    verifier = request.GET.get('verifier')
    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    token = request.GET.get('token')

    auth.request_token = {'oauth_token': token,
                          'oauth_token_secret': verifier}

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    api = tweepy.API(auth)

    user = api.get_user(user_id)

    #tweets = api.user_timeline(user_id)

    #for tweet in tweets:

    toxicity = {
        "name": user.screen_name,
        "toxicity": random.randint(180, 400),
    }

    return JsonResponse(toxicity, safe=False)
