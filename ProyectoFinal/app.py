import datetime
import json
import requests
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


@app.route('/post/<topic>', methods=['POST'])
def write_to_topic(topic):
    # make sure we have valid json
    json = request.get_json()
    client = get_kafka_client()
    topic = client.topics[topic.encode('ascii')]
    producer = topic.get_sync_producer()
    producer.send(topic, value=str.encode(json))
    return "OK"


@app.route("/addjson",  methods=["GET", "POST"])
def add_entry():
    """
    communication route for handling incoming vehicle data
    """
    if request.method == "POST":
        args = request.get_json()
    else:
        args = request.args
    if args:
        data = args
        data["timestamp"] = datetime.datetime.utcnow()

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
            prod.send('vehicle', value=str.encode(data))
        except Exception as e:
            print(e)

        return json.dumps(data)
    return dict(data="empty")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
