import json
import time
import datetime
from pymongo import MongoClient
from kafka import KafkaConsumer

# topic's name
KAFKA_TOPIC = "vehicle-events"
# assuming you have mongoDB installed locally
MONGO_HOST = 'mongodb://localhost:27017/vehicleeventsdb'

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers='localhost:9092')

for message in consumer:

    # This is the meat of the script...it connects to your mongoDB and stores the tweet
    try:

        client = MongoClient(MONGO_HOST)

        # Use vehicleeventsdb database. If it doesn't exist, it will be created.
        db = client.vehicleeventsdb

        # Decode the JSON from the vehicle
        datajson = json.loads(message.value.decode())

        # Add timestamp to message
        datajson['timestamp'] = datetime.datetime.now().isoformat()

        # Insert event message into the collection events
        db.events.insert(datajson)

        time.sleep(2)

    except Exception as e:
        print(e)
