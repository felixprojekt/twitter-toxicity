import os
import requests
import tweepy
from django.http import JsonResponse
from django.shortcuts import render


def user_toxicity(request, user_id):
    # verifier = request.GET.get('verifier')
    # token = request.GET.get('token')

    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    # auth.request_token = {'oauth_token': token,
    #                       'oauth_token_secret': verifier}

    try:
        # auth.get_access_token(verifier)
        auth.set_access_token(request.session['access_token'], request.session['access_token_secret'])
    except tweepy.TweepError:
        print('Error! Failed to retrieve access token from session.')

    api = tweepy.API(auth)

    user = api.get_user(user_id)

    toxicities = list()

    for tweet in api.user_timeline(user_id=user_id, count=3):
        r = analyze_tweet(request, tweet.text)
        if r:
            r = str(r)
            toxicities.append(float(r))

    if len(toxicities) != 0:
        average = sum(toxicities) / len(toxicities)
    else:
        average = 0

    toxicity = average * 200

    result = {
        "name": user.screen_name,
        "toxicity": toxicity,
    }

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
        return False


def insights(request):
    results = request.session.get('toxicities')

    # worst = sorted(results, key=lambda dct: dct['toxicity'])

    # worst = {k: sizes_sorted[k] for k in list(sizes_sorted)[:5]}

    context = {
        "worst": results,
    }

    return render(request, 'login/list-items.html', context)

