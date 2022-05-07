from kafka_producer import ACMEKafkaProducer
from file_writer import ACMEFileWriter
from datetime import datetime
import parcel_shipping_generator as ps_gen

PRODUCE_TO_KAFKA = True
WRITE_TO_FILE = False

EVENT_COUNT = 10000

if PRODUCE_TO_KAFKA:
    producer = ACMEKafkaProducer()
    start_time = datetime.now()
    for x in ps_gen.generate_parcel_data(EVENT_COUNT):
        producer.send(x)
    producer.flush()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
        end_time=(end_time-start_time).total_seconds()))

if WRITE_TO_FILE:
    writer = ACMEFileWriter()
    start_time = datetime.now()
    print('Generating Data')
    for x in ps_gen.generate_parcel_data(EVENT_COUNT):
        writer.write(x)
    print('Finished Generating Data')
    writer.upload_file()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
        end_time=(end_time-start_time).total_seconds()))
