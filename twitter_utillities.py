import tweepy
from twitter_credentials import *

def tweet(message):
    try:
        # Set up OAuth and integrate with API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Write a tweet to push to our Twitter account
        tweet = message
        api.update_status(status=tweet)
    except tweepy.TweepError:
        print("Message ERROR!: Unable to send message!")
