from __future__ import absolute_import, print_function

import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
from kafka import KafkaProducer
import time

KAFKA_TOPIC = "tweets"

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
access_token = "1385739478422142978-Aho4uhuOIvvary6jgnbUR5IrCO95mv"
access_token_secret = "cUBSLefXFpq8IuqMUxsTOs66zPeAZG6Ye3R9t1m49f4Gb"
api_key = "IAeW3AFMs2Hl25O1bVcGEJyno"
api_secret = "ihmKdShKEsurxuYyM3yD2Pyv9SEYMqZFHFdBqQCyMcfRjbhzEl"


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self):
        super().__init__()
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
    stream.filter(track=['medellin'])
