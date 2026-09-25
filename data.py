import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client("s3", region_name="us-west-2", config=Config(signature_version=UNSIGNED))
bucket = "amazon-last-mile-challenges"

for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])
        # s3.download_file(bucket, obj["Key"], obj["Key"].split("/")[-1])