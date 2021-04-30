from __future__ import absolute_import, print_function

import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
from kafka import KafkaProducer
import time

KAFKA_TOPIC = "tweets-topic"

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
api_key=""
api_secret=""
access_token=""
access_token_secret=""

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def on_data(self, data):
        # Send to kafka server.
        print('Tweet produced')
        time.sleep(2)
        self.producer.send(KAFKA_TOPIC, value=str.encode(data))
        self.producer.flush()

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit=True)

    stream = Stream(auth, l)
    #posts = api.user_timeline(screen_name="eafit",count=5,lang="en",tweet_mode="extended")
    #  Print the last 5 tweets
    print("Show the 5 recent tweets:\n")
    #i = 1
    #for tweet in posts[:5]:
        #print(str(i) + ') ' + tweet.full_text + '\n')
        #i = i+1
    stream.filter(track=['hola'])
