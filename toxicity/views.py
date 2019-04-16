import os
import random

import requests
import tweepy
from django.http import JsonResponse
from django.shortcuts import render


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

    toxicities = []

    for tweet in api.user_timeline(user_id=user_id, count=2):
        toxicities.append(analyze_tweet(request, tweet))

    toxicity = random.randint(180, 600)

    result = {
        "name": user.screen_name,
        "toxicity": toxicity,
    }

    return JsonResponse(result, safe=False)


def analyze_tweet(request):
    d = {
        'comment': {
            'text': 'what a stupid idea'
        },
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {}
        }
    }

    para = {
        "key": os.environ['PERSPECTIVE_KEY']
    }

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params=para,
        headers=headers, json=d)

    # return JsonResponse(r.json(), safe=False)

    rjson = r.json()

    return rjson['attributeScores']


def insights(request):
    sizes = request.session.get('toxicity')

    # sizes_sorted = sorted(sizes, key=lambda dct: dct['toxicity'])

    # worst = {k: sizes_sorted[k] for k in list(sizes_sorted)[:5]}

    context = {
        "worst": sizes,
    }

    return render(request, 'login/list-items.html', context)
