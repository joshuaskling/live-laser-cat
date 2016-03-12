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

#create api access point
api = tweepy.API(auth)

#post test pic
def postTestPic():
    api.update_with_media("content\\cat_test.jpg", "test status")

#stream class
class MyStreamListener(tweepy.StreamListener):
    
    #print stream
    def on_status(self, status):
        print(status.text.encode('utf-8'))
    
    #handle error codes
    def on_error(self, status_code):
        if (status_code == 420):
            return False

#create stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

#myStream.filter(follow="@LiveLaserCat", track=['test'], async=True)

#postTestPic()