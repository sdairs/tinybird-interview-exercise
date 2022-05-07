from kafka_producer import ACMEKafkaProducer
from datetime import datetime
import parcel_shipping_generator as ps_gen
#import file_writer

PRODUCE_TO_KAFKA=True
WRITE_TO_FILE=False

EVENT_COUNT=10000

if PRODUCE_TO_KAFKA:
    producer = ACMEKafkaProducer()
    start_time = datetime.now()
    for x in generator.generate_parcel_data(EVENT_COUNT):
        producer.send(x)
    producer.flush()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
    end_time=(end_time-start_time).total_seconds()))

# if WRITE_TO_FILE:
#     pass
