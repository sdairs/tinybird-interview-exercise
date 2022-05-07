from kafka import KafkaProducer
import json


class ACMEKafkaProducer():
    TOPIC = None
    BROKERS = None
    producer = None

    def __init__(self, broker_list='localhost:9092', topic='acme_shipping_parcel_status'):
        self.TOPIC = topic
        self.BROKERS = broker_list
        self.producer = KafkaProducer(bootstrap_servers=self.BROKERS,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def on_send_success(self, record_metadata):
        print('Successfully sent message {offset} to topic {topic} on partition {partition}'.format(
            offset=record_metadata.offset, topic=record_metadata.topic, partition=record_metadata.partition))

    def on_send_error(self, e):
        print('Failed to send message. Error: {e}'.format(e=e))

    def send(self, message):
        self.producer.send(self.TOPIC, message).add_callback(
            self.on_send_success).add_errback(self.on_send_error)

    def flush(self):
        self.producer.flush()
