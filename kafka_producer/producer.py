import json
import time
import requests
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'iss-location'

while True:
    res = requests.get("http://api.open-notify.org/iss-now.json")
    if res.status_code == 200:
        data = res.json()
        data['timestamp'] = time.time()
        print(f"[Producer] Sending: {data}")
        producer.send(topic, data)
    time.sleep(5)  # send data every 5 seconds
