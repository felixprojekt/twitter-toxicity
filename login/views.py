import os

from django.shortcuts import render, redirect
import tweepy


def index(request):
    del request.session['toxicities']

    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    request.session['request_token'] = auth.request_token

    context = {
        "redirect_url": redirect_url,
    }

    return render(request, 'login/index.html', context)


def result(request):
    verifier = request.GET.get('oauth_verifier')

    if verifier is None:
        return redirect("index")

    auth = tweepy.OAuthHandler(os.environ['TWITTER_KEY'], os.environ['TWITTER_SECRET'])

    token = request.GET.get('oauth_token')

    try:
        auth.request_token = {'oauth_token': token,
                              'oauth_token_secret': verifier}
    except tweepy.TweepError:
        print('Error! Failed to get request_token.')

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    request.session['access_token'] = auth.access_token
    request.session['access_token_secret'] = auth.access_token_secret

    api = tweepy.API(auth)

    context = {
        "ids": api.friends_ids()
    }

    return render(request, 'login/result.html', context)
