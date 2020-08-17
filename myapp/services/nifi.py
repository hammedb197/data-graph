from kafka import KafkaProducer
import json
import pprint

#kafka producer API for twitter data streaming
def send_topic(text):
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('nifi', key=b'text', value=text)
    

