import tweepy
import servo_driver, camera_driver

#set OAuth information
consumer_key = "Bb8BlQ8hFqaH6b5gqu4LPyRR1"
consumer_secret = "VmtljceTYOPLr3hvkvmhu7FQzLeLRxrrOK4LPv8GF5RFXADGyY"
access_token = "708766117678817280-ehanQvqL8LUnx15uvUXjJDynotWbaSz"
access_token_secret = "uCbdHeJ6jZkX2Bg7EAteKofhjYAnO5MP7h8xbMR6kuWVi"

#set authentications
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#run API
api = tweepy.API(auth)
public_tweets = api.home_timeline()

#print all tweets
for tweet in public_tweets:
    print (tweet.text)