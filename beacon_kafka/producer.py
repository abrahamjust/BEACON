import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

def send_event(event):
    producer.send(
        "beacon-events",
        event
    )
    producer.flush()
