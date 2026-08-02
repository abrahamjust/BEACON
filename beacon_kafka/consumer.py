import json
from kafka.consumer import KafkaConsumer

consumer = KafkaConsumer(
    "beacon-events",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    auto_offset_reset='earliest',
)

print("Listening....")

for message in consumer:
    print(message.value)