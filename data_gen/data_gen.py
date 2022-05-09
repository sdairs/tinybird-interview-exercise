from kafka_producer import ACMEKafkaProducer
from file_writer import ACMEFileWriter
from datetime import datetime
import parcel_shipping_generator as ps_gen
from dotenv import load_dotenv
import os
import sys

load_dotenv()

METHOD = os.environ.get('METHOD')
EVENT_COUNT = os.environ.get('EVENT_COUNT')

if EVENT_COUNT is None:
    EVENT_COUNT = 10000
else:
    try:
        EVENT_COUNT = int(EVENT_COUNT)
        if EVENT_COUNT < 0:
            raise RuntimeError
    except:
        print('ERROR: Ensure EVENT_COUNT is a valid positive integer')
        sys.exit(1)
if METHOD is None:
    raise RuntimeError(
        'No METHOD specified. You must configure a .env file with a valid METHOD of either "kafka" or "s3".')

if METHOD == 'kafka':
    producer = ACMEKafkaProducer()
    start_time = datetime.now()
    for x in ps_gen.generate_parcel_data(EVENT_COUNT):
        producer.send(x)
    producer.flush()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
        end_time=(end_time-start_time).total_seconds()))

elif METHOD == 's3':
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

else:
    print(f'METHOD value was not recognised: {METHOD}')
