import datetime
import json
import requests
import pymongo
from kafka import KafkaProducer, KafkaConsumer

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["kafka_consumer"] = KafkaConsumer(bootstrap_servers='localhost:9092')


def get_kafka_client(consumer=None):
    if consumer:
        return KafkaConsumer(bootstrap_servers='localhost:9092')
    return KafkaProducer(bootstrap_servers='localhost:9092')


@app.route('/topics/')
def topics():
    client = get_kafka_client(consumer=True)
    return jsonify([topic for topic in client.topics()])


@app.route("/addjson",  methods=["GET", "POST"])
def add_entry():
    """
    communication route for handling incoming vehicle data
    """
    if request.method == "POST":
        args = request.get_json()
    else:
        args = request.args.to_dict()
    if args:
        if float(args["latitude"]) > 0:
            data = args
            data["timestamp"] = str(datetime.datetime.utcnow())

            data["coords"] = (float(args["latitude"]), float(args["longitude"]))
            google_url = (
                    "https://maps.googleapis.com/maps/api/elevation/json?locations="
                    + str(args["latitude"])
                    + ","
                    + str(args["longitude"])
                    + "&key=AIzaSyChV7Sy3km3Fi8hGKQ8K9t7n7J9f6yq9cI"
            )

            r = requests.get(google_url).json()

            data["elevation"] = r["results"][0]["elevation"]
            try:
                prod = get_kafka_client()
                prod.send('vehicle-events', value=json.dumps(data).encode("utf-8"))
            except Exception as e:
                print(e)

            return json.dumps(data)
        args["status"] = "invalid location"
        return json.dumps(args)
    return dict(data="empty")


@app.route("/mongodb/events-count", methods=["GET"])
def get_events_in_mongodb():
    """
    Return the number of events in the mongodb database 'vehicleevents'
    in the collection 'events'.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["vehicleeventsdb"]
    events = db.get_collection("events")
    return str(events.find().count())


if __name__ == "__main__":
    app.run(debug=True, port=8080)
