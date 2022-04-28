# Tinybird Demo
This is a demo for [Tinybird](https://tinybird.co).

# What's included

This demo includes:
- Generation of fake data (& file upload to S3)
  - `data_gen/generate.py` Simulated parcel shipping data in `ndjson` format
- Tinybird data source using the fake data
  - An HTTP URL source that loads the file from S3 
- Tinybird pipes that expose the data via API
  - `parcel_tracking_raw` exposes the raw data feed
  - `parcel_tracking_delivered_count` exposes the current count of delivered parcels
  - `parcel_tracking_latest_status` exposes the latest status of each parcel, with an optional filter for a specific parcel ID

# Getting started

## Requirements

The following python packages are required:

```
boto3
tinybird-cli
```


## Installation

Install the requirements with

 `pip install -r requirements.txt`

## Setup

### AWS

#### S3

First, create an S3 bucket to use for the demo (or you can reuse an existing bucket).

This demo will create a prefix of `tinybird/fake` in this bucket.

#### IAM

Next, create or find an IAM User that has appropriate permissions to Get & Put in your S3 bucket.

Finally, [create an access key](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/) for this IAM User.

Keep the Access Key and Secret Key handy for the next step.

### Generate.py

Edit `data_gen/generate.py` to add your AWS credentials, S3 bucket details and optionally configure the amount of events you'd like to generate.

You should find this section at the top of the file:

```
##
# SET YOUR AWS KEYS HERE
##
SECRET_KEY = '' # Your IAM User Secret Key
ACCESS_KEY = '' # Your IAM User Access Key
REGION = '' # Your AWS Region
S3_BUCKET = '' # Your AWS bucket name (without the s3:// prefix)
EVENT_COUNT=10000 # How many events to generate
```

Fill in the fields with your environment details, such that it looks like the following example:

```
##
# SET YOUR AWS KEYS HERE
##
SECRET_KEY = 'fjghsdffjkDFfsg+hfkjgfdh77guwrjnd' # Your IAM User Secret Key
ACCESS_KEY = 'ALFDJKFBD74FDNBF793' # Your IAM User Access Key
REGION = 'eu-west-1' # Your AWS Region
S3_BUCKET = 'tinybird-test' # Your AWS bucket name (without the s3:// prefix)
EVENT_COUNT=10000 # How many events to generate
```

Make sure to save the file after editing.

## Running

Start by generating the fake data.

Run

`python data_gen/generate.py`

Once complete, check that your S3 bucket contains the file, for example:

`tinybird/fake/2022_01_01_00:00:00.ndjson`

