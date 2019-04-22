import os
import requests
import tweepy
import json
import operator
import collections
from django.http import JsonResponse
from django.shortcuts import render


def user_toxicity(request, user_id):
    # verifier = request.GET.get('verifier')
    # token = request.GET.get('token')

    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    # auth.request_token = {'oauth_token': token,
    #                       'oauth_token_secret': verifier}

    try:
        # auth.get_access_token(verifier) # probably not the best idea
        auth.set_access_token(request.session['access_token'], request.session['access_token_secret'])
    except tweepy.TweepError:
        print('Error! Failed to retrieve access token from session.')

    api = tweepy.API(auth)

    user = api.get_user(user_id)

    toxicities = list()

    for tweet in api.user_timeline(user_id=user_id, count=1):
        print('Analyzing: ' + tweet.text)
        r = analyze_tweet(request, tweet.text)
        if isinstance(r, float):
            print('Result of analyze_tweet: ' + str(r))
            toxicities.append(r)
        elif isinstance(r, dict):
            print('Result of analyze_tweet is object:')
            print(json.dumps(r))

    if len(toxicities) != 0:
        average = sum(toxicities) / len(toxicities)
    else:
        average = 0

    toxicity = average * 200

    result = {
        "name": user.screen_name,
        "toxicity": toxicity,
    }

    if 'toxicities' not in request.session:
        print('Creating toxicities dict')
        request.session['toxicities'] = {}

    request.session['toxicities'][user.screen_name] = toxicity
    request.session.modified = True
    print("Current session value: " + json.dumps(request.session['toxicities']))

    return JsonResponse(result, safe=False)


def analyze_tweet(request, tweet_text):
    d = {
        'comment': {
            'text': tweet_text
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

    if 'attributeScores' in r.json():
        return r.json()['attributeScores']['TOXICITY']['summaryScore']['value']
    else:
        return r.json()


def insights(request):
    results = request.session.get('toxicities')

    sorted_list = sorted(results.items(), key=lambda kv: kv[1])

    sorted_dict = collections.OrderedDict(sorted_list)

    best = dict(sorted_dict.items()[:5])
    worst = dict(sorted_dict.items()[-5:])

    print('Best: ' + json.dumps(best))
    print('Worst: ' + json.dumps(worst))

    context = {
        "worst": worst,
        "best": best,
    }

    return render(request, 'login/list-items.html', context)

