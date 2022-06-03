from kafka import KafkaProducer
from dotenv import load_dotenv
import certifi
import json
import os


class ACMEKafkaProducer():
    TOPIC = None
    BROKERS = None
    SECURITY_PROTOCOL = None
    SASL_MECHANISM = None
    USER = None
    PASSWORD = None

    producer = None

    def __init__(self):
        load_dotenv()
        self.TOPIC = os.environ.get('KAFKA_TOPIC')
        self.BROKERS = os.environ.get('KAFKA_BROKERS')
        self.SECURITY_PROTOCOL = os.environ.get('KAFKA_SECURITY_PROTOCOL')
        self.SASL_MECHANISM = os.environ.get('KAFKA_SASL_MECHANISM')
        self.USER = os.environ.get('KAFKA_USER')
        self.PASSWORD = os.environ.get('KAFKA_PASSWORD')

        if self.SECURITY_PROTOCOL == 'PLAINTEXT' or self.SECURITY_PROTOCOL is None:
            self.producer = KafkaProducer(bootstrap_servers=self.BROKERS,
                                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        elif self.SECURITY_PROTOCOL in ['SASL_PLAINTEXT', 'SASL_SSL']:
            if self.SASL_MECHANISM is None:
                raise RuntimeError(
                    'You must configure a sasl.mechanism when using SASL_PLAINTEXT or SASL_SSL')
            if self.USER is None or self.PASSWORD is None:
                raise RuntimeError(
                    'You must specify a user & password for authentication.')
            if self.SASL_MECHANISM == 'PLAIN':
                self.producer = KafkaProducer(bootstrap_servers=self.BROKERS,
                                              value_serializer=lambda v: json.dumps(
                                                  v).encode('utf-8'),
                                              security_protocol=self.SECURITY_PROTOCOL, sasl_mechanism=self.SASL_MECHANISM,
                                              sasl_plain_username=self.USER, sasl_plain_password=self.PASSWORD,
                                              ssl_cafile=certifi.where())
            else:
                raise NotImplementedError(
                    'Only PLAIN sasl.mechanism is supported.')
        else:
            raise NotImplementedError(
                'Only SASL_PLAINTEXT and SASL_SSL security.protocols are supported.')

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
