import os
import json
import boto3
from botocore.exceptions import ClientError

BUCKET = os.getenv("S3_BUCKET_NAME", "appmk3")
KEY = os.getenv("S3_DB_KEY", "database.json")

# S3 client will use env vars AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
s3 = boto3.client("s3")

def read_s3_db():
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=KEY)
        return json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return []
        raise

def write_s3_db(data):
    s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))
