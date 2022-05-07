# import boto3
# from botocore.exceptions import ClientError
# import datetime
# import os
# import json
# import parcel_shipping_generator as ps_gen

# ##
# # SET YOUR AWS KEYS HERE
# ##
# SECRET_KEY = ''  # Your IAM User Secret Key
# ACCESS_KEY = ''  # Your IAM User Access Key
# REGION = ''  # Your AWS Region
# S3_BUCKET = ''  # Your AWS bucket name (without the s3:// prefix)

# EVENT_COUNT = 10000  # How many events to generate


# dir_path = os.path.dirname(os.path.realpath(__file__))


# # Generate & write to local file
# with open(dir_path+'/data/output.txt', 'w') as f:
#     start_time = datetime.datetime.now()
#     for x in ps_gen.generate_parcel_data(EVENT_COUNT):
#         f.write(json.dumps(x)+'\n')
#     end_time = datetime.datetime.now()
#     print('Took {end_time} seconds'.format(
#         end_time=(end_time-start_time).total_seconds()))


# def upload_file():
#     # Uploaded generated file to S3
#     s3 = boto3.client(
#         's3',
#         region_name=REGION,
#         aws_access_key_id=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY
#     )
#     try:
#         print('Uploading to S3')
#         response = s3.upload_file(dir_path+'/data/output.txt', S3_BUCKET,
#                                   'tinybird/fake/'+str(datetime.datetime.now())+'.ndjson'.replace(' ', '_'))
#         print('Finished uploading')
#         print(response)
#     except ClientError as e:
#         return False
#     return True