
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("S3_ACCESS_KEY") or None,
        aws_secret_access_key=os.getenv("S3_SECRET_KEY") or None,
        region_name=os.getenv("S3_REGION") or None
    )

def upload_file(local_path, bucket, key):
    s3 = get_s3_client()
    s3.upload_file(local_path, bucket, key)
    return key

def generate_presigned_put(bucket, key, expires_in=3600):
    s3 = get_s3_client()
    return s3.generate_presigned_url('put_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires_in)
