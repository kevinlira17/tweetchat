
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *

# Variables that contains the user credentials to access Twitter API 
access_token = '64570827-oNAvcxk9F9y9tplfENm5faCmpcLaO5mIqsav3SMPL'
access_token_secret = 'MT8NLOrAo2uT9481V8IsXpYug30Ri5vyVsCprxE57zNRI'
consumer_key = 'SJsvNkN8SkbYZNdzisPiyXi0D'
consumer_key_secret = '5SiP0nWhCHmwhOEEwC30799GKPuRV6egblGW3Ov1EFUUqpGa55'

#oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(domain='stream.twitter.com', auth=OAuth(access_token, access_token_secret, consumer_key,  consumer_key_secret))

# Get a sample of the public data following through Twitter

# copy and paste these: 🙂🙁👍👎
iterator = twitter_stream.statuses.filter(track="🙂", language="en")

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 1
for tweet in iterator:
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    stringtweet = json.dumps(tweet)
    data = json.loads(stringtweet)
    if "text" in data:
        text = data["text"]
        # we want no overlap with out tweets
        if "🙁" not in text and "👍" not in text and "👎" not in text and "🙂" in text:
            print(text)
            # save to file placeholder
            tweet_count -= 1
    
    # The command below will do pretty printing for JSON data, try it out
    #print(json.dumps(tweet, indent=4))
       
    if tweet_count <= 0:
        break 
