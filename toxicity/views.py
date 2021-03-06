import os
import requests
import tweepy
import json
import operator
import collections
from django.http import JsonResponse
from django.shortcuts import render


def user_toxicity(request, user_id):
    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    try:
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
        # print('Creating toxicities dict')
        request.session['toxicities'] = {}

    request.session['toxicities'][user.screen_name] = toxicity
    request.session.modified = True
    # print("Current session value: " + json.dumps(request.session['toxicities']))

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
    context = get_worst_and_best_friends(request)

    return render(request, 'login/list-items.html', context)


def worst_friends(request):
    friends_dict = get_worst_and_best_friends(request)

    friends_list = list()

    for key in friends_dict['worst']:
        friends_list.append('@' + key)

    return JsonResponse(friends_list, safe=False)


def get_worst_and_best_friends(request):
    results = request.session.get('toxicities')

    sorted_list = sorted(results.items(), key=lambda kv: kv[1])

    best = sorted_list[:5]
    worst = sorted_list[-5:]
    worst.reverse()

    best_dict = collections.OrderedDict(best)
    worst_dict = collections.OrderedDict(worst)

    friends = {
        "best": best_dict,
        "worst": worst_dict,
    }

    return friends
