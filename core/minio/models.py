import minio
from minio import Minio
from minio.error import S3Error
import settings
import json
from loggers import logger


client = Minio(
    settings.MINIO_CONFIG.end_point,
    access_key=settings.MINIO_CONFIG.access_key,
    secret_key=settings.MINIO_CONFIG.secret_key,
    secure=False
)
bucket = settings.MINIO_CONFIG.bucket


def init_minio():
    if not client.bucket_exists(bucket_name=bucket):
        client.make_bucket(bucket_name=bucket)
        # https://min.io/docs/minio/linux/developers/python/API.html#set_bucket_policy
        client.delete_bucket_policy(bucket)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": f"arn:aws:s3:::{bucket}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket}/*",
                },
            ],
        }
        client.set_bucket_policy(bucket, json.dumps(policy))

        bucket_policy = client.get_bucket_policy(bucket_name=bucket)
        logger.debug(bucket_policy)


try:
    init_minio()
except Exception as error:
    logger.exception(error)

if __name__ == '__main__':
    init_minio()
