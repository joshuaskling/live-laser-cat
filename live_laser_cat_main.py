import tweepy, praw, requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import servo_driver, camera_driver

#set OAuth information
consumer_key = "qNfUHr4XUyoaeTapyMyk7quYG"
consumer_secret = "0gRguuOwK5t3YuyhAJIxny5JMoaV8Hon6mioNUnGdCTEjpfe2W"
access_token = "708766117678817280-ehanQvqL8LUnx15uvUXjJDynotWbaSz"
access_token_secret = "uCbdHeJ6jZkX2Bg7EAteKofhjYAnO5MP7h8xbMR6kuWVi"

#set authentications
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#create api access point
api = tweepy.API(auth)

#get top posts from showerthoughts and aww
def getRedditContent():
    print("Getting Reddit content")
    r = praw.Reddit(user_agent="livelasercat")

    #get submissions
    print("Getting image...")
    submissions = r.get_random_submission('aww')

    url = submissions.url
    print (url)
    #for x in submissions:
    #    url = x.url

    #download image to local machine
    image = open("temp.jpg", "wb")
    image.write(requests.get(url).content)
    image.close()
    print("Image downloaded")

    #get text
    text = ""
    print("Getting showerthought...")
    submissions = r.get_random_submission('showerthoughts')

    #for item in submissions:
    #    text = item
    text = str(submissions).split(":: ")
    text = text[1]
    print (text)
    #print ("Showerthought downloaded")

    #apply text to picture
    print ("Applying text to image...")

    #define fonts
    font = ImageFont.truetype("C:\Windows\\Fonts\\Calibri.ttf",40)
    textColor = (255, 255, 255)
    textPosition = (100,100)

    #open image and draw
    image = Image.open("temp.jpg")
    draw = ImageDraw.Draw(image)
    draw.text(textPosition, text, fill=textColor, font=font)
    del draw

    #save image
    image.save("temp.jpg")
    image.close()


#post cat photo (currently in test mode)
def postNewPhoto(user):
    input = user.decode('utf-8')
    api.update_with_media("content\\cat_test.jpg", "Cat photo taken for @" + input)

#stream class
class MyStreamListener(tweepy.StreamListener):
    
    #print stream
    def on_status(self, status):
        print(status.author.screen_name.encode('utf-8') + status.source.encode('utf-8') + status.text.encode('utf-8'))
        postNewPhoto(status.author.screen_name.encode('utf-8'))
    
    #handle error codes
    def on_error(self, status_code):
        if (status_code == 420):
            print ("test")
            return False
            
getRedditContent()

#create stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

#run stream
myStream.filter(track=['@livelasercat'], async=True)

"""    
#main loop method checks for messages every x minutes
while(1):
    #set timer
    if (sent == True):
        timer = time.clock()
        sent = False
    
    #get direct messages at interval
    if (time.clock() - timer > 10):
        messages = api.direct_messages()
        for message in messages:
            print (message)
        
        #check for new messages
        #if new message, send data
        postNewPhoto("@testuser")
"""
"""
#print all tweets
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)
"""