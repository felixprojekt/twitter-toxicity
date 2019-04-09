import os
import random
from pprint import pprint
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

    result = {
        "name": user.screen_name,
        "toxicity": toxicity,
    }

    request.session['toxicity'][user.screen_name] = toxicity

    return JsonResponse(result, safe=False)


def insights(request):

    sizes = request.session.get('toxicity')

    # sizes_sorted = sorted(sizes, key=lambda dct: dct['toxicity'])

    # worst = {k: sizes_sorted[k] for k in list(sizes_sorted)[:5]}

    context = {
        "worst": sizes,
    }

    return render(request, 'login/list-items.html', context)
