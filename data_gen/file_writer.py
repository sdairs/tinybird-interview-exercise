import boto3
from botocore.exceptions import ClientError
import datetime
import os
import json
import parcel_shipping_generator as ps_gen
from dotenv import load_dotenv

class ACMEFileWriter():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, path=None):
        load_dotenv()
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.ACCESS_KEY = os.environ.get('ACCESS_KEY')
        self.REGION = os.environ.get('REGION')
        self.S3_BUCKET = os.environ.get('S3_BUCKET')
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
