import json
import time
from pymongo import MongoClient
from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
    'tweets',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers='localhost:9092')

for message in consumer:
    print(message)

# This is the meat of the script...it connects to your mongoDB and stores the tweet
# try:
#
#     client = MongoClient(MONGO_HOST)
#
#     # Use twitterdb database. If it doesn't exist, it will be created.
#     db = client.twitterdb
#
#     # Decode the JSON from Twitter
#     datajson = json.loads(message.value.decode())
#
#     # grab the 'created_at' data from the Tweet to use for display
#     created_at = datajson['created_at']
#
#     # print out a message to the screen that we have collected a tweet
#     print("Tweet collected at " + str(created_at))
#
#     # insert the data into the mongoDB into a collection called twitter_search
#     # if twitter_search doesn't exist, it will be created.
#     db.twitter_search.insert(datajson)
#
#     time.sleep(2)
#
# except Exception as e:
#     print(e)
