from kafka.kafka_producer import ACMEKafkaProducer
from file.s3_writer import ACMEFileWriter
from datetime import datetime
import parcel_shipping_generator as ps_gen
from dotenv import load_dotenv
import os
import sys

load_dotenv()

METHOD = os.environ.get('METHOD')
MAX_DAYS = os.environ.get('MAX_DAYS')
PARCELS_PER_DAY = os.environ.get('PARCELS_PER_DAY')

if MAX_DAYS is None:
    MAX_DAYS = 100
elif PARCELS_PER_DAY is None:
    PARCELS_PER_DAY = 1000

try:
    MAX_DAYS = int(MAX_DAYS)
    PARCELS_PER_DAY = int(PARCELS_PER_DAY)
    if MAX_DAYS <= 0:
        raise Exception('MAX_DAYS')
    if PARCELS_PER_DAY <= 0:
        raise Exception('PARCELS_PER_DAY')
except Exception as e:
    print(f'ERROR: Ensure MAX_DAYS & PARCELS_PER_DAY are valid positive integer')
    sys.exit(1)

if METHOD is None:
    raise RuntimeError(
        'No METHOD specified. You must configure a .env file with a valid METHOD of either "kafka" or "s3".')

if METHOD == 'kafka':
    producer = ACMEKafkaProducer()
    start_time = datetime.now()
    for x in ps_gen.generate_parcel_data(max_days=MAX_DAYS, parcels_per_day=PARCELS_PER_DAY):
        producer.send(x)
    producer.flush()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
        end_time=(end_time-start_time).total_seconds()))

elif METHOD == 's3':
    writer = ACMEFileWriter()
    start_time = datetime.now()
    print('Generating Data')
    for x in ps_gen.generate_parcel_data(max_days=MAX_DAYS, parcels_per_day=PARCELS_PER_DAY):
        writer.write(x)
    print('Finished Generating Data')
    writer.upload_file()
    end_time = datetime.now()
    print('Took {end_time} seconds'.format(
        end_time=(end_time-start_time).total_seconds()))

else:
    print(f'METHOD value was not recognised: {METHOD}')
