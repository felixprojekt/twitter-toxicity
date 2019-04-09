import os
import random

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

    toxicity = random.randint(180, 600)



    #tweets = api.user_timeline(user_id)

    #for tweet in tweets:

    result = {
        "name": user.screen_name,
        "toxicity": toxicity,
    }

    request.session['toxicity'] = result

    return JsonResponse(result, safe=False)


def insights(request):

    sizes = request.session.get('toxicity')

    # sizes_sorted = sorted(sizes, key=lambda dct: dct['toxicity'])

    # worst = {k: sizes_sorted[k] for k in list(sizes_sorted)[:5]}

    context = {
        "worst": sizes
    }

    return render(request, 'login/list-items.html', context)
