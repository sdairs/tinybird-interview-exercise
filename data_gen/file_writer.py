import boto3
from botocore.exceptions import ClientError
import datetime
import os
import json
import parcel_shipping_generator as ps_gen


class ACMEFileWriter():
    SECRET_KEY = ''
    ACCESS_KEY = ''
    REGION = ''
    S3_BUCKET = ''

    dir_path = os.path.dirname(os.path.realpath(__file__))

    path = None

    def __init__(self, path=None):
        if path is None:
            self.path = self.dir_path+'/data/output.txt'
        if os.path.exists(self.path):
            os.remove(self.path)

    def write(self, message):
        with open(self.path, 'a') as f:
            f.write(json.dumps(message)+'\n')
            f.close()

    def upload_file(self):
        # Uploaded generated file to S3
        s3 = boto3.client(
            's3',
            region_name=self.REGION,
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY
        )
        try:
            print('Uploading to S3.')
            _ = s3.upload_file(self.path, self.S3_BUCKET,
                               'tinybird/fake/'+str(datetime.datetime.now())+'.ndjson'.replace(' ', '_'))
            print('Finished uploading.')
        except ClientError as e:
            return False
        return True
