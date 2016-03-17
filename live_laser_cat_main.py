import tweepy, praw, requests, textwrap, random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import servo_driver, camera_driver

#temp user
tempUser = "JoshuaKling".encode('utf-8')

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
def getRedditContent(user):
    print("Getting Reddit content")
    r = praw.Reddit(user_agent="livelasercat")

    #get submissions
    print("Getting image...")
    submissions = r.get_subreddit('earthporn').get_hot(limit=20)
    images = []

    #url = submissions.url
    #print (url)
    for x in submissions:

        if ("imgur.com/" in x.url and ".jpg" in x.url):
            images.append(x.url)
            #url = x.url

    #download random image to local machine
    image = open("temp.jpg", "wb")
    image.write(requests.get(images[random.randrange(0, len(images))]).content)
    image.close()
    print("Image downloaded")

    #get text
    text = ""
    print("Getting showerthought...")
    submissions = r.get_random_submission('showerthoughts')

    text = submissions.title
    print ("Showerthought downloaded")

    #apply text to picture
    print ("Applying text to image...")

    #open image
    image = Image.open("temp.jpg")

    #chop text for wrapping
    width, height = image.size
    text = textwrap.wrap(text, int(width/30), break_long_words=False)
    print (text)

    #define fonts
    font = ImageFont.truetype("C:\Windows\\Fonts\\Tahoma.ttf", 50)
    textColor = (random.randrange(200,255), random.randrange(200,255), random.randrange(200,255))
    shadowColor = (0,0,0)

    offset = height/15
    textPositionx = 100
    textPositiony = height - 400

    draw = ImageDraw.Draw(image)

    #apply text to image
    for x in text:
        #apply border
        draw.text((textPositionx-1, textPositiony), x, font=font, fill=shadowColor)
        draw.text((textPositionx+1, textPositiony), x, font=font, fill=shadowColor)
        draw.text((textPositionx, textPositiony-1), x, font=font, fill=shadowColor)
        draw.text((textPositionx, textPositiony+1), x, font=font, fill=shadowColor)

        draw.text((textPositionx, textPositiony), x, fill=textColor, font=font)
        textPositiony = textPositiony + offset
    del draw

    #save image
    image.save("temp.jpg")
    image.close()

    #send photo
    postRedditPhoto(user)
    print ("Photo sent!")

#post reddit photo
def postRedditPhoto(user):
    input = user.decode('utf-8')
    api.update_with_media("temp.jpg", "Shower thoughts for @" + input)

#post cat photo (currently in test mode)
def postNewPhoto(user):
    input = user.decode('utf-8')
    api.update_with_media("content\\cat_test.jpg", "Cat photo taken for @" + input)

#stream class
class MyStreamListener(tweepy.StreamListener):
    
    #print stream
    def on_status(self, status):
        print(status.author.screen_name.encode('utf-8') + status.source.encode('utf-8') + status.text.encode('utf-8'))
        #postNewPhoto(status.author.screen_name.encode('utf-8'))
        getRedditContent(status.author.screen_name.encode('utf-8'))
    
    #handle error codes
    def on_error(self, status_code):
        if (status_code == 420):
            print ("test")
            return False

#getRedditContent(tempUser)

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