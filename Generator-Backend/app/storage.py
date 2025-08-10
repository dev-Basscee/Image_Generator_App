import os
import boto3
from botocore.config import Config
from io import BytesIO

BUCKET = os.getenv("S3_BUCKET")
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    region_name=os.getenv("S3_REGION", "us-east-1"),
    config=Config(signature_version="s3v4"),
)

def put_object(key: str, data: bytes, content_type: str = "image/png"):
    S3_CLIENT.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType=content_type)


def presigned_url(key: str, expires: int = 86400) -> str:
    return S3_CLIENT.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )